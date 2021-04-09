@.str.0 = private unnamed_addr constant [3 x i8] c"%i\00", align 1

declare i32 @printf(i8*, ...)
define i32 @main() {
    start:

; we exit with code 0 = success
ret i32 0
}
