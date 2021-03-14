declare i32 @printf(i8*, ...)
@.str = private unnamed_addr constant [3 x i8] c"%i\00", align 1

define i32 @main() {
    start:
          %a = alloca i32, align 4
          store i32 %0, i32* %a
          %1 = load i32, i32* %a
          %2 = add i32 %1, 1
          store i32 %2, i32* %a
    ; everything below is for debugging
          %3 = load i32, i32* %a
          %p = call i32 (i8*, ...)
               @printf(i8* getelementptr inbounds ([8 x i8],
                                                   [8 x i8]* @format,
                                                   i32 0, i32 0),
                       i32 %3)
    ; we exit with code 0 = success
          ret i32 0
}
