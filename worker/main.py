from worker.runtime.worker_runtime import WorkerRuntime
def main():
    runtime = WorkerRuntime()

    runtime.run()
if __name__ == '__main__':
    main()