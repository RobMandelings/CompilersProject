@.str.0 = private unnamed_addr constant [5 x i8] c"%d\n\00", align 1
declare dso_local i32 @printf(i8*, ...)

define dso_local i32 @main() {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = srem i32 7, 2
  store i32 %3, i32* %1, align 4
  %4 = load i32, i32* %1, align 4
  %5 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.0, i64 0, i64 0), i32 %4)
  ret i32 1

6:
  %7 = load i32, i32* %2, align 4
  ret i32 %7

}
