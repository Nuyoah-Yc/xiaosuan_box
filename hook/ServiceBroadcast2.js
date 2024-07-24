Java.perform(function() {
    var isLoging = false;
    var classLoaders = Java.enumerateClassLoadersSync();

    class LogMessage {
        constructor() {
            this.messages = [];
        }

        add(...msg) {
            this.messages.push(msg.join(' '));
        }

        send() {
            while (true) {
                if (!isLoging) {
                    isLoging = true;
                    try {
                        this.messages.forEach(message => console.log(message));
                    } catch (e) {
                        console.log("输出时发生了异常");
                        console.error('Caught exception:', e.message);
                    }
                    isLoging = false;
                    break;
                }
            }
        }
    }

    function currentTime() {
        const currentDate = new Date();
        return `Current time: ${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()} ${currentDate.getHours()}:${currentDate.getMinutes()}:${currentDate.getSeconds()}.${currentDate.getMilliseconds()}`;
    }

    function loadClass(className) {
        if (typeof className === "string") {
            try {
                return Java.use(className);
            } catch (e) {
                for (let i = 0; i < classLoaders.length; i++) {
                    try {
                        return classLoaders[i].loadClass(className);
                    } catch (e) {
                        if (i + 1 === classLoaders.length) {
                            console.log("无法找到类", className);
                        }
                    }
                }
            }
        } else {
            return className;
        }
    }

    function hook(className, methodName, onum = 0, filter = null, custom = null) {
        var targetClass = loadClass(className);

        targetClass[methodName].overloads[onum].implementation = function() {
            let print = new LogMessage();
            let argsInfo = { thiz: this, printer: print, args: arguments, pb: false, ret: 0 };

            let flag = filter ? filter(argsInfo) : true;

            if (custom) {
                custom(argsInfo);
            }

            if (argsInfo.pb) {
                return argsInfo.ret;
            }

            var res = this[methodName].apply(this, arguments);

            if (flag) {
                print.send();
            }

            return res;
        };
    }

    function dumpIntent(intent) {
        let output = ' Extras(';
        let extras = intent.getExtras();
        if (!extras) {
            return ' Extras()';
        }
        extras.keySet().toArray().forEach(key => {
            let value = intent.getExtra(key);
            output += `${key}=${value} `;
        });
        return output + ')';
    }

    function logMethodCall(args, callType, intentIndex, packageNameIndex) {
        let intent = args[intentIndex];
        let callpkg = args[packageNameIndex];
        let data = dumpIntent(intent);
        if (!callpkg) {
            callpkg = "null/Android";
        }
        let output = `[${callpkg}] ${callType}: ${intent.toString()}${data}`;
        args.printer.add(output + '\n');
    }

    hook("com.android.server.am.ActivityManagerService", "broadcastIntentLocked", 1, null, (args) => {
        logMethodCall(args, 'sending Broadcast', 3, 1);
    });

    hook("com.android.server.am.ActiveServices", "bindServiceLocked", 0, null, (args) => {
        logMethodCall(args, 'Binding service', 2, 0);
    });

    hook("com.android.server.am.ActiveServices", "startServiceLocked", 1, null, (args) => {
        logMethodCall(args, 'Starting service', 1, 0);
    });

    hook("com.android.server.am.ActivityManagerService", "getContentProvider", 0, null, (args) => {
        let callpkg = args[1];
        let provider = args[2];
        args.printer.add(`[${callpkg}] getProvider: ${provider}\n`);
    });

    hook("com.android.server.wm.ActivityTaskManagerService", "startActivityAsUser", 0, null, (args) => {
        logMethodCall(args, 'startActivityAsUser', 3, 1);
    });

    hook("com.android.server.wm.ActivityTaskManagerService", "startActivityIntentSender", 0, null, (args) => {
        let caller = args[0];
        let target = args[1];
        args.printer.add(`[${caller}] startActivityIntentSender: ${target}\n`);
    });
});
