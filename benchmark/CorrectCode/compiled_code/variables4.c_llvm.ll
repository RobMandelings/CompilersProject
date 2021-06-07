@.str.0 = private unnamed_addr constant [3 x i8] c"%d\00", align 1
declare dso_local i32 @printf(i8*, ...)

define dso_local i32 @main() {
  %1 = alloca i32, align 4
  %2 = alloca i32*, align 4
  %3 = alloca i32, align 4
  store i32 10, i32* %1, align 4
  store i32* %1, i32** %2, align 4
  %4 = load i32*, i32** %2, align 4
  %5 = load i32, i32* %4, align 4
  %6 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.0, i64 0, i64 0), i32 %5)
  %7 = load i32, i32* %3, align 4
  ret i32 %7

}
