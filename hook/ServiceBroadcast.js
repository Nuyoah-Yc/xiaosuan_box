Java.perform(function(){
    var isLoging = false
    var classLoaders = Java.enumerateClassLoadersSync();


    //线程互斥封装
    class logMessage{
        constructor(){
            this.Messages = new Array();
        } 
        add(...msg){
            var msg2 = ''
            msg.forEach((item) => msg2=msg2+item)
            this.Messages.push(msg2)
        }
        send(){
            while(true){
                if(isLoging==false){
                    isLoging=true
                    try{
                        for(var i=0;i<this.Messages.length;i++){
                            console.log(this.Messages[i])
                        }
                    }catch(e){
                        console.log("输出时发生了异常")
                        console.error('Caught exception:', e.message);
                    }
                    isLoging=false
                    break
                }
            } 
        }
    }

    function currentTime(){
        const currentDate = new Date();

        const year = currentDate.getFullYear();
        const month = currentDate.getMonth() + 1;
        const day = currentDate.getDate();
        const hours = currentDate.getHours();
        const minutes = currentDate.getMinutes();
        const seconds = currentDate.getSeconds();
        const milliseconds = currentDate.getMilliseconds();

        return `Current time: ${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${milliseconds}`;
    }

    function loadclass(className){
        if(typeof className === "string"){
            try{
                var test = Java.use(className)
            }catch(e){
                for(let i=0;i<classLoaders.length;i++){
                    try{
                        var test = classLoaders[i].loadClass(className)
                        break
                    }catch(e){
                        if(i+1 == classLoaders.length){
                            console.log("无法找到类",className)
                        }
                    }
                }
            }
        }else{
            var test = className
        }

        return test
    }


    var hook = function(className,methodName,onum=0,filter=null,custom=null){
        
        var test = loadclass(className)
        
        test[methodName].overloads[onum].implementation = function(){
            let print = new logMessage()
            let aargument = {thiz:this,printer:print,args:arguments,pb:false,ret:0}
            if(filter!=null){
                var flag = filter(aargument)
            }else{
                var flag =true
            }
            if(custom!=null){
                custom(aargument)
            }

            if(aargument.pb){
                return aargument.ret
            }
            
            var res = this[methodName].apply(this,arguments);
            
            if(flag){
                print.send()
            }
            
            return res
        }
    }

    function dumpIntent(intent){
        let output=' Extras('
        let extras = intent.getExtras()
        if(extras==null){
            return ' Extras()'
        }
        extras.keySet().toArray().forEach((key)=>{
            let value = intent.getExtra(key)
            output = output+key+'='+value+' '
        })
        return output+')'
    }


    hook("com.android.server.am.ActivityManagerService","broadcastIntentLocked",1,null,
    (arg)=>{
        let callpkg = arg.args[1]
        let intent = arg.args[3]
        let data = dumpIntent(intent)
        if(callpkg==null){
            callpkg = "null/Andoird"
        }
        let output = "["+callpkg+"] sending Broadcast "+intent.toString()+data
        arg.printer.add(output+'\n')

        // if(intent.getPackage()=="com.google.android.apps.photos" && intent.getAction()=="com.google.android.gms.phenotype.UPDATE"){
        //     arg.pb=true
        //     arg.ret=0
        // }
    })

    hook("com.android.server.am.ActiveServices","bindServiceLocked",0,null,
    (arg)=>{
        let intent = arg.args[2]
        let data = dumpIntent(intent)
        let callerapp = arg.thiz.mAm.value.getRecordForAppLOSP(arg.args[0])
        let callpkg = callerapp.info.value.packageName.value
        let output = "["+callpkg+"] Binding service "+intent.toString()+data
        arg.printer.add(output+'\n')

        if(callpkg=="com.google.android.apps.photos" && intent.getAction() == "com.google.android.gms.phenotype.service.START"){
            arg.pb=true
            arg.ret=0
        }
    })

    hook("com.android.server.am.ActiveServices","startServiceLocked",1,null,
    (arg)=>{
        let intent = arg.args[1]
        let data = dumpIntent(intent)
        let callerapp = arg.thiz.mAm.value.getRecordForAppLOSP(arg.args[0])
        if(callerapp==null){
            var callpkg = "null/Android"
        }else{
            var callpkg = callerapp.info.value.packageName.value
        }
        let output = "["+callpkg+"] Starting service "+intent.toString()+data
        arg.printer.add(output+'\n')
    })

    hook("com.android.server.am.ActivityManagerService","getContentProvider",0,null,
    (arg)=>{
        let callpkg = arg.args[1]
        let provider = arg.args[2]
        arg.printer.add("["+callpkg+"] getProvider: "+provider+"\n")
    })

    hook("com.android.server.wm.ActivityTaskManagerService","startActivityAsUser",0,null,
    (arg)=>{
        let callpkg = arg.args[1]
        let intent = arg.args[3]
        arg.printer.add("["+callpkg+"] startActivityAsUser: "+intent+"\n")
    }
    )

    hook("com.android.server.wm.ActivityTaskManagerService","startActivityIntentSender",0,null,
    (arg)=>{
        let caller = arg.args[0]
        let target = arg.args[1]
        arg.printer.add("["+caller+"] startActivityIntentSender: "+target+"\n")
    }
    )
});