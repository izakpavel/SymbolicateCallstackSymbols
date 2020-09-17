# SymbolicateCallstackSymbols
Script to symbolicate logs obtained by *Thread.callStackSymbols*

## Why? What?
In my project, I am using custom log files containing various information about app behaviour and in case of exception, each such exception is being logged together with callstack backtrace using `Thread.callStackSymbols.joined(separator: "\n")`

When in trouble, user can export these logs from the app, but the callstack dump is not symbolized. With this simple Python script that internally calls `atos` tool it is easy to go through the log file and symbolicate the callstacks.

__This script does not depend on any file structure, so it should work with any custom log file.__ Only those lines that contain callstack output are being processed.

## Usage
* copy your app, dsym file and log file ideally into the same folder
* call `python3 symbolicate.py -l <log_filename> -n <app_name>` to get symbolicated output
* you do not need to provide directory nor any architecture if you are ok with default values (./, arm64)

## Example
* part of log file
```
... 
🔵 Info 2020-08-16 07:48:16 +0000 <NSThread: 0x2822fd300>{number = 1, name = main} /Users/pavelzak/MyApp
🔵 Info 2020-08-16 11:01:21 +0000 <NSThread: 0x280ce8d40>{number = 1, name = main} /Users/pavelzak/MyApp/model/RemoteNotificationsResolver.swift userNotificationCenter(_:willPresent:withCompletionHandler:) at:50 -> will present notification with unknown category

🔴 Error 2020-08-15 13:25:11 +0000 <NSThread: 0x280ad0bc0>{number = 1, name = main} /Users/pavelzak/MyApp/swiftCommon/ErrorPresentable.swift showAlert(error:handler:) at:27 -> Error Domain=cz.pavelzak.myapp Code=153 "(null)"
 callstack: 
0   MyApp                               0x000000010087a7e4 MyApp + 1697764
1   MyApp                               0x0000000100879738 MyApp + 1693496
2   MyApp                               0x000000010085b694 MyApp + 1570452
3   MyApp                               0x00000001008e1204 MyApp + 2118148
4   MyApp                               0x0000000100874a60 MyApp + 1673824
5   MyApp                               0x00000001008739ac MyApp + 1669548
6   MyApp                               0x0000000100819054 MyApp + 1298516
7   libdispatch.dylib                   0x000000019fe829a8 5A83D0CF-8FB9-3727-8A32-012D20A47EC8 + 371112
8   libdispatch.dylib                   0x000000019fe83524 5A83D0CF-8FB9-3727-8A32-012D20A47EC8 + 374052
9   libdispatch.dylib                   0x000000019fe355b4 5A83D0CF-8FB9-3727-8A32-012D20A47EC8 + 54708
10  CoreFoundation                      0x00000001a013b748 409609CD-8410-38E1-BA5D-BDED609D2018 + 689992
11  CoreFoundation                      0x00000001a013661c 409609CD-8410-38E1-BA5D-BDED609D2018 + 669212
12  CoreFoundation                      0x00000001a0135c34 CFRunLoopRunSpecific + 424
13  GraphicsServices                    0x00000001aa27f38c GSEventRunModal + 160
14  UIKitCore                           0x00000001a426822c UIApplicationMain + 1932
15  MyApp                               0x00000001007b3aac MyApp + 883372
16  libdyld.dylib                       0x000000019ffbd800 876FB49A-BFBA-37BF-AD37-6FFC90F7F981 + 6144
...
```

* symbolicated output
```
🔵 Info 2020-08-16 07:48:16 +0000 <NSThread: 0x2822fd300>{number = 1, name = main} /Users/pavelzak/MyApp
🔵 Info 2020-08-16 11:01:21 +0000 <NSThread: 0x280ce8d40>{number = 1, name = main} /Users/pavelzak/MyApp/model/RemoteNotificationsResolver.swift userNotificationCenter(_:willPresent:withCompletionHandler:) at:50 -> will present notification with unknown category

🔴 Error 2020-08-15 13:25:11 +0000 <NSThread: 0x280ad0bc0>{number = 1, name = main} /Users/pavelzak/MyApp/swiftCommon/ErrorPresentable.swift showAlert(error:handler:) at:27 -> Error Domain=cz.pavelzak.myapp Code=153 "(null)"
0   specialized LogService.LogDefaultFormatter.formatMessage(_:logLevel:file:function:line:) (in MyApp) (LogService.swift:100)
1   LogService.logError(_:file:function:line:) (in MyApp) (LogService.swift:113)
2   specialized ErrorPresentable<>.showAlert(error:handler:) (in MyApp) (<compiler-generated>:0)
3   closure #3 in MyAppViewController.viewDidLoad() (in MyApp) (<compiler-generated>:0)
4   specialized MyAppViewModel.requestTask(_:didFailWithError:) (in MyApp) (<compiler-generated>:0)
5   @objc MyAppViewModel.requestTask(_:didFailWithError:) (in MyApp) (<compiler-generated>:0)
6   __27-[RequestTask didFailWithError]_block_invoke (in MyApp) (RequestTask.m:239)
7   libdispatch.dylib                   0x000000019fe829a8 5A83D0CF-8FB9-3727-8A32-012D20A47EC8 + 371112
8   libdispatch.dylib                   0x000000019fe83524 5A83D0CF-8FB9-3727-8A32-012D20A47EC8 + 374052
9   libdispatch.dylib                   0x000000019fe355b4 5A83D0CF-8FB9-3727-8A32-012D20A47EC8 + 54708
10  CoreFoundation                      0x00000001a013b748 409609CD-8410-38E1-BA5D-BDED609D2018 + 689992
11  CoreFoundation                      0x00000001a013661c 409609CD-8410-38E1-BA5D-BDED609D2018 + 669212
12  CoreFoundation                      0x00000001a0135c34 CFRunLoopRunSpecific + 424
13  GraphicsServices                    0x00000001aa27f38c GSEventRunModal + 160
14  UIKitCore                           0x00000001a426822c UIApplicationMain + 1932
15  main (in MyApp) (main.m:13)
16  libdyld.dylib                       0x000000019ffbd800 876FB49A-BFBA-37BF-AD37-6FFC90F7F981 + 6144
```
