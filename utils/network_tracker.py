class NetworkTracker:

    @staticmethod
    def inject(driver):
        driver.execute_script("""
            if (!window.__networkTrackerInstalled) {
                window.__networkTrackerInstalled = true;
                window.pendingRequests = 0;

                const origFetch = window.fetch;
                if (origFetch) {
                    window.fetch = function() {
                        window.pendingRequests++;
                        return origFetch.apply(this, arguments).finally(() => {
                            window.pendingRequests--;
                        });
                    };
                }

                const origOpen = XMLHttpRequest.prototype.open;
                XMLHttpRequest.prototype.open = function() {
                    this.addEventListener("readystatechange", function() {
                        if (this.readyState === 1) window.pendingRequests++;
                        if (this.readyState === 4) window.pendingRequests--;
                    }, false);
                    origOpen.apply(this, arguments);
                };
            }
        """)
