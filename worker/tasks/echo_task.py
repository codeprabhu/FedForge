class EchoTask:
    def execute(self, payload: dict):
        return {
            "message": payload["message"]
        }