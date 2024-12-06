# -------- auto-reconnectable - still asynchronous

class AutoReconnectProtocol:

    ### refer to a SidecarProtocol instance, but by composition
    # so that we can re-create that object when a connection comes down
    def __init__(self, url, *args, **kwds):
        self.url = url
        self.args = args
        self.kwds = kwds
        self.proto = None

    async def connect(self):
        await self.close()
        self.proto = SidecarProtocol(url, *self.args, **self.kwds)

    async def close(self):
        if self.proto:
            logger.info("closing zombie proto")
            try:
                await self.proto.close()
            except Exception:
                logger.exception("ignored when cleaning up during reconnect")



    async def send(self, *args, **kwds):
        logger.info("superseded send..")
        try:
            return await super().send(*args, **kwds)
        except websockets.exceptions.ConnectionClosed as exc:
            print(f"received exception {type(exc)} : {exc}")





class SidecarAsyncMagic(websockets.client.connect):

    def __init__(self, url, *args, **kwds):
        if 'create_protocol' in kwds:
            logging.error("should not overwrite create_protocol")
        super().__init__(url, create_protocol=AutoReconnectProtocol,
                         *args, **kwds)
