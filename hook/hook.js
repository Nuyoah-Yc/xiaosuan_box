const commonPaths = [
    "/data/local/bin/su",
    "/data/local/su",
    "/data/local/xbin/su",
    "/dev/com.koushikdutta.superuser.daemon/",
    "/sbin/su",
    "/system/app/Superuser.apk",
    "/system/bin/failsafe/su",
    "/system/bin/su",
    "/su/bin/su",
    "/system/etc/init.d/99SuperSUDaemon",
    "/system/sd/xbin/su",
    "/system/xbin/busybox",
    "/system/xbin/daemonsu",
    "/system/xbin/su",
    "/system/sbin/su",
    "/vendor/bin/su",
    "/cache/su",
    "/data/su",
    "/dev/su",
    "/system/bin/.ext/su",
    "/system/usr/we-need-root/su",
    "/system/app/Kinguser.apk",
    "/data/adb/magisk",
    "/sbin/.magisk",
    "/cache/.disable_magisk",
    "/dev/.magisk.unblock",
    "/cache/magisk.log",
    "/data/adb/magisk.img",
    "/data/adb/magisk.db",
    "/data/adb/magisk_simple",
    "/init.magisk.rc",
    "/system/xbin/ku.sud",
    "/data/adb/ksu",
    "/data/adb/ksud"
];

const ROOTmanagementApp = [
    "com.noshufou.android.su",
    "com.noshufou.android.su.elite",
    "eu.chainfire.supersu",
    "com.koushikdutta.superuser",
    "com.thirdparty.superuser",
    "com.yellowes.su",
    "com.koushikdutta.rommanager",
    "com.koushikdutta.rommanager.license",
    "com.dimonvideo.luckypatcher",
    "com.chelpus.lackypatch",
    "com.ramdroid.appquarantine",
    "com.ramdroid.appquarantinepro",
    "com.topjohnwu.magisk",
    "me.weishu.kernelsu",
    "com.noshufou.android.su",
    "com.noshufou.android.su.elite",
    "eu.chainfire.supersu",
    "com.koushikdutta.superuser",
    "com.thirdparty.superuser",
    "com.yellowes.su",
    "com.koushikdutta.rommanager",
    "com.koushikdutta.rommanager.license",
    "com.dimonvideo.luckypatcher",
    "com.chelpus.lackypatch",
    "com.ramdroid.appquarantine",
    "com.ramdroid.appquarantinepro",
    "com.topjohnwu.magisk",
    "com.kingroot.kinguser",
    "com.kingo.root",
    "com.smedialink.oneclickroot",
    "com.zhiqupk.root.global",
    "com.alephzain.framaroot",
    "com.android.vending.billing.InAppBillingService.COIN",
    "com.android.vending.billing.InAppBillingService.LUCK",
    "com.chelpus.luckypatcher",
    "com.blackmartalpha",
    "org.blackmart.market",
    "com.allinone.free",
    "com.repodroid.app",
    "org.creeplays.hack",
    "com.baseappfull.fwd",
    "com.zmapp",
    "com.dv.marketmod.installer",
    "org.mobilism.android",
    "com.android.wp.net.log",
    "com.android.camera.update",
    "cc.madkite.freedom",
    "com.solohsu.android.edxp.manager",
    "org.meowcat.edxposed.manager",
    "com.xmodgame",
    "com.cih.game_cih",
    "com.charles.lpoqasert",
    "catch_.me_.if_.you_.can_"
];


function stackTraceHere(isLog) {
    var Exception = Java.use('java.lang.Exception');
    var Log = Java.use('android.util.Log');
    var stackinfo = Log.getStackTraceString(Exception.$new())
    if (isLog) {
        console.log(stackinfo)
    } else {
        return stackinfo
    }
}

function stackTraceNativeHere(isLog) {
    var backtrace = Thread.backtrace(this.context, Backtracer.ACCURATE)
        .map(DebugSymbol.fromAddress)
        .join("\n\t");
    console.log(backtrace)
}


function bypassJavaFileCheck() {
    var UnixFileSystem = Java.use("java.io.UnixFileSystem")
    UnixFileSystem.checkAccess.implementation = function (file, access) {

        var stack = stackTraceHere(false)

        const filename = file.getAbsolutePath();

        if (filename.indexOf("magisk") >= 0) {
            console.log("Anti Root Detect - check file: " + filename)
            return false;
        }

        if (commonPaths.indexOf(filename) >= 0) {
            console.log("Anti Root Detect - check file: " + filename)
            return false;
        }

        return this.checkAccess(file, access)
    }
}

function bypassNativeFileCheck() {
    var fopen = Module.findExportByName("libc.so", "fopen")
    Interceptor.attach(fopen, {
        onEnter: function (args) {
            this.inputPath = args[0].readUtf8String()
        },
        onLeave: function (retval) {
            if (retval.toInt32() != 0) {
                if (commonPaths.indexOf(this.inputPath) >= 0) {
                    console.log("Anti Root Detect - fopen : " + this.inputPath)
                    retval.replace(ptr(0x0))
                }
            }
        }
    })

    var access = Module.findExportByName("libc.so", "access")
    Interceptor.attach(access, {
        onEnter: function (args) {
            this.inputPath = args[0].readUtf8String()
        },
        onLeave: function (retval) {
            if (retval.toInt32() == 0) {
                if (commonPaths.indexOf(this.inputPath) >= 0) {
                    console.log("Anti Root Detect - access : " + this.inputPath)
                    retval.replace(ptr(-1))
                }
            }
        }
    })
}

function setProp() {
    var Build = Java.use("android.os.Build")
    var TAGS = Build.class.getDeclaredField("TAGS")
    TAGS.setAccessible(true)
    TAGS.set(null, "release-keys")

    var FINGERPRINT = Build.class.getDeclaredField("FINGERPRINT")
    FINGERPRINT.setAccessible(true)
    FINGERPRINT.set(null, "google/crosshatch/crosshatch:10/QQ3A.200805.001/6578210:user/release-keys")

    // Build.deriveFingerprint.inplementation = function(){
    //     var ret = this.deriveFingerprint() //该函数无法通过反射调用
    //     console.log(ret)
    //     return ret
    // }

    var system_property_get = Module.findExportByName("libc.so", "__system_property_get")
    Interceptor.attach(system_property_get, {
        onEnter(args) {
            this.key = args[0].readCString()
            this.ret = args[1]
        },
        onLeave(ret) {
            if (this.key == "ro.build.fingerprint") {
                var tmp = "google/crosshatch/crosshatch:10/QQ3A.200805.001/6578210:user/release-keys"
                var p = Memory.allocUtf8String(tmp)
                Memory.copy(this.ret, p, tmp.length + 1)
            }
        }
    })

}

//android.app.PackageManager
function bypassRootAppCheck() {
    var ApplicationPackageManager = Java.use("android.app.ApplicationPackageManager")
    ApplicationPackageManager.getPackageInfo.overload('java.lang.String', 'int').implementation = function (str, i) {
        // console.log(str)
        if (ROOTmanagementApp.indexOf(str) >= 0) {
            console.log("Anti Root Detect - check package : " + str)
            str = "ashen.one.ye.not.found"
        }
        return this.getPackageInfo(str, i)
    }

    //shell pm check
}

function bypassShellCheck() {
    var String = Java.use('java.lang.String')

    var ProcessImpl = Java.use("java.lang.ProcessImpl")
    ProcessImpl.start.implementation = function (cmdarray, env, dir, redirects, redirectErrorStream) {

        if (cmdarray[0] == "mount") {
            console.log("Anti Root Detect - Shell : " + cmdarray.toString())
            arguments[0] = Java.array('java.lang.String', [String.$new("")])
            return ProcessImpl.start.apply(this, arguments)
        }

        if (cmdarray[0] == "getprop") {
            console.log("Anti Root Detect - Shell : " + cmdarray.toString())
            const prop = [
                "ro.secure",
                "ro.debuggable"
            ];
            if (prop.indexOf(cmdarray[1]) >= 0) {
                arguments[0] = Java.array('java.lang.String', [String.$new("")])
                return ProcessImpl.start.apply(this, arguments)
            }
        }

        if (cmdarray[0].indexOf("which") >= 0) {
            const prop = [
                "su"
            ];
            if (prop.indexOf(cmdarray[1]) >= 0) {
                console.log("Anti Root Detect - Shell : " + cmdarray.toString())
                arguments[0] = Java.array('java.lang.String', [String.$new("")])
                return ProcessImpl.start.apply(this, arguments)
            }
        }

        return ProcessImpl.start.apply(this, arguments)
    }
}


function hook1() {
    Java.perform(function () {
        var AlertDialogBuilder = Java.use('androidx.appcompat.app.AlertDialog$Builder');

        AlertDialogBuilder.setMessage.overload('java.lang.CharSequence').implementation = function (message) {
            console.log("Original message: " + message);

            message = Java.use('java.lang.String').$new("Hello from Frida!!!!!!!!!!!!!");
            var result = this.setMessage(message);

            return result;
        };
    });
}

function hook2() {
    Java.perform(function () {
        var SplashScreenActivity = Java.use("ticketek.com.au.ticketek.ui.splashscreen.SplashScreenActivity");

        SplashScreenActivity.u0.implementation = function (str) {
            console.log("u0 called with: " + str);

            // Print the Java stack trace
            console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));

            // Call the original implementation
            var result = this.u0.apply(this, arguments);

            return result;
        };
    });
}


function hook3() {
    Java.perform(function () {
        // Hook 'Thread' 类的 'setDefaultUncaughtExceptionHandler' 方法
        // var Thread = Java.use('java.lang.Thread');
        // Thread.setDefaultUncaughtExceptionHandler.implementation = function (handler) {
        //     // 当 'setDefaultUncaughtExceptionHandler' 被调用时，打印 handler 对象
        //     console.log('setDefaultUncaughtExceptionHandler called with handler: ' + handler.$className);
        //     // 继续执行原始的 'setDefaultUncaughtExceptionHandler' 方法
        //     return this.setDefaultUncaughtExceptionHandler(handler);
        // };

        // Hook 'Thread$UncaughtExceptionHandler' 接口的 'uncaughtException' 方法
        var UncaughtExceptionHandler = Java.use('java.lang.Thread$UncaughtExceptionHandler');
        UncaughtExceptionHandler.uncaughtException.implementation = function (thread, exception) {
            // 当 'uncaughtException' 被调用时，打印线程信息和异常信息
            console.log('uncaughtException called on thread: ' + thread + ' with exception: ' + exception);
            // 打印异常的消息内容
            console.log('Exception message: ' + exception.getMessage());
            // 打印异常的堆栈跟踪
            console.log('Exception stack trace: ' + Java.use('android.util.Log').getStackTraceString(exception));
            // 继续执行原始的 'uncaughtException' 方法
            return this.uncaughtException(thread, exception);
        };

        // Hook 'Process' 类的 'killProcess' 方法
        var Process = Java.use('android.os.Process');
        Process.killProcess.implementation = function (pid) {
            // 当 'killProcess' 被调用时，打印进程ID
            console.log('killProcess called with PID: ' + pid);
            // 打印当前的调用栈信息
            console.log('Call stack:\n' + Java.use('android.util.Log').getStackTraceString(Java.use('java.lang.Exception').$new()));
            // 继续执行原始的 'killProcess' 方法
            return this.killProcess(pid);
        };
    });

}

function hook4() {
    Java.perform(function () {
        var RuntimeInit = Java.use('com.android.internal.os.RuntimeInit');
        var KillApplicationHandler = Java.use('com.android.internal.os.RuntimeInit$KillApplicationHandler');
        var Log = Java.use('android.util.Log');

        // Hook com.android.internal.os.RuntimeInit$KillApplicationHandler.uncaughtException 方法
        KillApplicationHandler.uncaughtException.implementation = function (thread, throwable) {
            // 获取调用者信息
            var caller = Java.use('java.lang.Thread').currentThread();
            var callerClass = caller.getClass().toString();
            var callerId = caller.getId();
            var callerName = caller.getName();

            // 打印调用者信息
            console.log('com.android.internal.os.RuntimeInit$KillApplicationHandler.uncaughtException called by:');
            console.log('Caller Class: ' + callerClass);
            console.log('Caller ID: ' + callerId);
            console.log('Caller Name: ' + callerName);

            // 打印调用栈
            var stackTrace = Log.getStackTraceString(throwable);
            console.log('Stack Trace:\n' + stackTrace);

            // 执行原始的 uncaughtException 方法
            this.uncaughtException(thread, throwable);
        }
    });

}

function hook5() {
    Java.perform(function () {
        // 定位到 n5 类
        var n5Class = Java.use('sa.virginmobile.vm.util.n5');

        // Hook n5.e 方法，始终返回false以绕过root检测
        n5Class.e.implementation = function (context) {
            console.log('Root detection check bypassed');
            return false; // 返回false表示未检测到root
        };

        // Hook n5.d 方法，始终返回false以绕过debug模式检测
        // n5Class.d.implementation = function (context) {
        //     console.log('Debug mode detection check bypassed');
        //     return false; // 返回false表示未检测到debug模式
        // };
    });
}


function hook6() {
    Interceptor.attach(Module.findExportByName("libc.so", "open"), {
        onEnter: function (args) {
            // 读取原始路径
            var originalPath = Memory.readCString(args[0]);
            console.log("原始打开文件路径：" + originalPath);

            // 判断路径中是否包含关键词"status"
            if (originalPath.includes("20492/status")) {
                // if (originalPath.includes("libimmune.so")) {
                console.log("路径包含'status'，将被重定向");

                // 设置新的路径
                var newPath = "/data/local/tmp/status";
                var allocMemory = Memory.allocUtf8String(newPath);
                args[0] = allocMemory;

                console.log("重定向后的路径：" + newPath);
            }
        },
        onLeave: function (retval) {
            if (retval.toInt32() === -1) {
                console.error("文件打开失败，错误码：" + retval.toInt32());
            } else {
                console.log("文件成功打开，文件描述符：" + retval.toInt32());
            }
        }
    });
}

function hook7() {
    Java.perform(function () {
        var Activity = Java.use("com.cherrypicks.hsbcpayme.view.a$b");  // 使用内部类路径

        // 重写 onReceive 方法
        Activity.onReceive.implementation = function (context, intent) {
            console.log("Broadcast Received: " + intent.getAction());

            // 检查 intent 和 action
            if (intent !== null && intent.getAction() !== null) {
                var action = intent.getAction();

                // 检查是否是我们关心的特定行动
                if (action.equals(Java.use("yrhcxcuj.aj").a(3196))) {
                    console.log("Detected target action: " + action);

                    // 检查是否报告了 Frida 的存在
                    if (intent.hasExtra("ARGUMENT_FRIDA_DETECTED")) {
                        var isFridaDetected = intent.getBooleanExtra("ARGUMENT_FRIDA_DETECTED", false);
                        console.log("Frida Detected Flag: " + isFridaDetected);

                        // 如果检测到 Frida，修改结果避免触发安全操作
                        if (isFridaDetected) {
                            console.log("Frida detection broadcast received, ignoring it.");
                            return;  // 不执行 m7() 和其他任何操作
                        }
                    }
                }
            }

            // 原始方法调用
            this.onReceive(context, intent);
        };
    });

}


function hook8() {
    Java.perform(function () {
        let GoogleOAuthFlow = Java.use("com.wikiloc.wikilocandroid.mvvm.oauth_login.model.GoogleOAuthFlow");
        GoogleOAuthFlow["getUserCredentials"].implementation = function (data) {
            console.log(`GoogleOAuthFlow.getUserCredentials is called: data=${data}`);
            let result = this["getUserCredentials"](data);
            console.log(`GoogleOAuthFlow.getUserCredentials result=${result}`);
            return result;
        };
    });
}


function main() {
    console.log("通用过root检测已经启用")
    bypassNativeFileCheck()
    bypassJavaFileCheck()
    setProp()
    bypassRootAppCheck()
    bypassShellCheck()
    // hook1();
    // hook2();
    // hook3();
    // hook4();
    // hook5();
    // hook6();
    // hook7();
    hook8();
}


setImmediate(main);
