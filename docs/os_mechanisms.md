# OS Mechanisms: Centralized Dashboard

## Concurrency and Threading
The main API gateway utilizes `socketserver.ThreadingMixIn` combined with `HTTPServer`. This allows the operating system to spawn a new thread for every incoming HTTP POST or GET request. This multithreaded architecture acts as a load balancer, ensuring the server does not crash during live data spikes from 50 runners.

## Resource Locks and Synchronization
To prevent race conditions when multiple threads write to the central database, the system uses a strict OS Mutex via `threading.Lock()`. The `db_lock` object ensures only one thread can access and modify `central_db.json` at any given time.