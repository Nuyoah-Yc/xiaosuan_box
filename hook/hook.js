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


function hook2() {
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


function hook3() {
    Java.perform(function () {
        console.log("Starting script...");

        // 获取 Build 类
        var Build = Java.use("android.os.Build");

        // 钩住 Build 类的 TAGS 字段
        var TAGSField = Build.class.getDeclaredField("TAGS");
        TAGSField.setAccessible(true);


        // 打印原始 TAGS 字段的值
        console.log("Original TAGS: " + Build.TAGS.value);

        // 修改 TAGS 字段的值
        // TAGSField.set(null, "custom_tags");

        // 验证修改是否成功
        // console.log("Modified TAGS: " + Build.TAGS.value);
    });

}

function hook4() {
    // 加载 Frida 模块
    Java.perform(function () {
        let t = Java.use("com.paytmbank.walletnew.utilitycommon.t");
        t["Z"].implementation = function (context) {
            console.log(`t.Z is called: context=${context}`);
            let result = this["Z"](context);
            console.log(`t.Z result=${result}`);
            return false;
        };
    });
}

function hook5() {
    Java.perform(function () {
        let PaytmActivity = Java.use("net.one97.paytm.activity.PaytmActivity");
        let Log = Java.use("android.util.Log");
        let Exception = Java.use("java.lang.Exception");

        PaytmActivity["doIntegrityChecks"].implementation = function () {
            console.log(`PaytmActivity.doIntegrityChecks is called`);
            console.log(Log.getStackTraceString(Exception.$new()));
            // Call the original method if needed
            // this["doIntegrityChecks"]();


        };
    });
}

function hook6() {
    Java.perform(function () {
        var LliClass = Java.use('lli');
        var lkgClass = Java.use('lkg');
        var BundleClass = Java.use('android.os.Bundle');

        lkgClass.f.overload('atkz', 'aqnj', 'gwt', 'gvf').implementation = function (atkzArg, aqnjArg, gwtArg, gvfArg) {
            console.log('f method called with arguments:');
            console.log('atkz: ' + atkzArg);
            console.log('aqnj: ' + aqnjArg);
            console.log('gwt: ' + gwtArg);
            console.log('gvf: ' + gvfArg);

            console.log('atkz details: ' + atkzArg);
            var atjjClass = Java.use('atjj');
            if (atkzArg.$className === 'atjj') {
                var atjjObject = Java.cast(atkzArg, atjjClass);
                printAtjjDetails(atjjObject, 0);
            }

            var aqnjClass = Java.use('aqnj');
            var aqnjObject = Java.cast(aqnjArg, aqnjClass);
            var aqnjFields = aqnjClass.class.getDeclaredFields();
            for (var i = 0; i < aqnjFields.length; i++) {
                var field = aqnjFields[i];
                field.setAccessible(true);
                console.log('aqnj field: ' + field.getName() + ' = ' + field.get(aqnjObject));
            }

            // 检查 gwt 对象的类名并进行强制转换
            console.log('gwt details: ' + gwtArg);
            console.log('gwt class: ' + gwtArg.$className);
            try {
                var gwtClass = Java.use(gwtArg.$className);
                var gwtObject = Java.cast(gwtArg, gwtClass);
                var gwtFields = gwtClass.class.getDeclaredFields();
                for (var i = 0; i < gwtFields.length; i++) {
                    var field = gwtFields[i];
                    field.setAccessible(true);
                    console.log('gwt field: ' + field.getName() + ' = ' + field.get(gwtObject));
                }
                var gwtMethods = gwtClass.class.getDeclaredMethods();
                for (var i = 0; i < gwtMethods.length; i++) {
                    var method = gwtMethods[i];
                    console.log('gwt method: ' + method.getName());
                }
            } catch (e) {
                console.log('Error casting gwt: ' + e);
            }

            var gvfClass = Java.use('gvf');
            var gvfObject = Java.cast(gvfArg, gvfClass);
            var gvfFields = gvfClass.class.getDeclaredFields();
            for (var i = 0; i < gvfFields.length; i++) {
                var field = gvfFields[i];
                field.setAccessible(true);
                console.log('gvf field: ' + field.getName() + ' = ' + field.get(gvfObject));
            }

            var result = this.f(atkzArg, aqnjArg, gwtArg, gvfArg);
            console.log('f method result: ' + result);

            return result;
        };

        LliClass.c.implementation = function (s, bundle0, aqnj0) {
            console.log('c method called with arguments:');
            console.log('String s: ' + s);
            console.log('Bundle bundle0: ' + bundle0);
            console.log('aqnj aqnj0: ' + aqnj0);

            console.log('Bundle bundle0 contents:');
            var bundleKeys = bundle0.keySet().toArray();
            for (var i = 0; i < bundleKeys.length; i++) {
                var key = bundleKeys[i];
                console.log('bundle0[' + key + ']: ' + bundle0.get(key));
            }

            console.log('aqnj aqnj0 contents:');
            var aqnjClass = Java.use('aqnj');
            var aqnjObject = Java.cast(aqnj0, aqnjClass);
            var aqnjFields = aqnjClass.class.getDeclaredFields();
            for (var i = 0; i < aqnjFields.length; i++) {
                var field = aqnjFields[i];
                field.setAccessible(true);
                console.log('aqnj0 field: ' + field.getName() + ' = ' + field.get(aqnjObject));
            }

            var result = this.c(s, bundle0, aqnj0);
            console.log('c method result: ' + result);
            return result;
        };

        function printAtjjDetails(atjjObject, depth) {
            if (depth > 10) {
                console.log('Max depth reached, stopping recursion.');
                return;
            }

            var atjjFields = atjjObject.class.getDeclaredFields();
            for (var i = 0; i < atjjFields.length; i++) {
                var field = atjjFields[i];
                field.setAccessible(true);
                console.log('atjj field (depth ' + depth + '): ' + field.getName() + ' = ' + field.get(atjjObject));

                if (field.getName() === 'setFuture') {
                    var setFuture = field.get(atjjObject);
                    if (setFuture && setFuture.$className) {
                        console.log('setFuture details (depth ' + depth + '): ' + setFuture);
                        var atjjClass = Java.use('atjj');
                        if (setFuture.$className === 'atjj') {
                            var innerAtjjObject = Java.cast(setFuture, atjjClass);
                            printAtjjDetails(innerAtjjObject, depth + 1);
                        }
                    }
                }
            }
        }
    });
}


function hook7() {
    Java.perform(function () {
        let kjg = Java.use("kjg");
        kjg["$init"].overload('lmh', 'llg', 'java.lang.String', 'android.os.Bundle', 'gvf', 'int').implementation = function (lmhVar, llgVar, str, bundle, gvfVar, i) {
            console.log(`kjg.$init is called: lmhVar=${lmhVar}, llgVar=${llgVar}, str=${str}, bundle=${bundle}, gvfVar=${gvfVar}, i=${i}`);
            this["$init"](lmhVar, llgVar, str, bundle, gvfVar, i);
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
    hook7();
}


main()
