"""
Copyright [2024] [Xuxin Cheng, Jialong Li]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import asyncio
import json
import os
ROOT = os.path.dirname(__file__)

from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.rtcrtpsender import RTCRtpSender
from aiortc import MediaStreamTrack
from av import VideoFrame
import time
import cv2
import matplotlib.pyplot as plt
from multiprocessing import shared_memory
import numpy as np
from concurrent.futures import ThreadPoolExecutor

class ZedVideoTrack(MediaStreamTrack):
    kind = "video"
    def __init__(self, img_shape, shm_name):
        super().__init__()  # Initialize base class
        self.img_shape = (img_shape[0], 2*img_shape[1], 3)
        self.img_height, self.img_width = img_shape[:2]

        # Create shared memory access in executor to avoid blocking
        self.existing_shm = shared_memory.SharedMemory(name=shm_name)
        self._executor = ThreadPoolExecutor(max_workers=1)

        self.timescale = 1000  # Use a timescale of 1000 for milliseconds
        self.frame_interval = 1 / 30
        self._last_frame_time = time.time()
        self.start_time = time.time()
    
    async def recv(self):
        now = time.time()
        wait_time = self._last_frame_time + self.frame_interval - now
        if wait_time > 0:
            await asyncio.sleep(wait_time)
            # print("Waited for: ", wait_time)
        self._last_frame_time = time.time()

        # Run potentially blocking shared memory operations in executor
        frame = await asyncio.get_event_loop().run_in_executor(
            self._executor,
            lambda: np.ndarray(
                (self.img_shape[0], self.img_shape[1], 3), 
                dtype=np.uint8, 
                buffer=self.existing_shm.buf
            ).copy()
        )
        
        av_frame = VideoFrame.from_ndarray(frame, format='rgb24')  # Convert numpy array to AVFrame
        timestamp = int((time.time() - self.start_time) * self.timescale)
        av_frame.pts = timestamp
        av_frame.time_base = self.timescale
        # print("Time to process frame: ", time.time() - start)
        return av_frame
    
def force_codec(pc, sender, forced_codec):
    kind = forced_codec.split("/")[0]
    codecs = RTCRtpSender.getCapabilities(kind).codecs
    transceiver = next(t for t in pc.getTransceivers() if t.sender == sender)
    transceiver.setCodecPreferences(
        [codec for codec in codecs if codec.mimeType == forced_codec]
    )


async def index(request):
    content = open(os.path.join(ROOT, "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def javascript(request):
    content = open(os.path.join(ROOT, "client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)

class RTC():
    def __init__(self, img_shape, shm_name, fps) -> None:
        self.img_shape = img_shape
        self.shm_name = shm_name
        self.fps = fps
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    async def offer(self, request):
        params = await request.json()
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

        pc = RTCPeerConnection()
        pcs.add(pc)

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            print("Connection state is %s" % pc.connectionState)
            if pc.connectionState == "failed":
                await pc.close()
                pcs.discard(pc)

        zed_track = ZedVideoTrack(self.img_shape, self.shm_name)
        video_sender = pc.addTrack(zed_track)

        force_codec(pc, video_sender, "video/H264")

        await pc.setRemoteDescription(offer)

        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return web.Response(
            content_type="application/json",
            text=json.dumps(
                {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
            ),
        )


pcs = set()

async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()
