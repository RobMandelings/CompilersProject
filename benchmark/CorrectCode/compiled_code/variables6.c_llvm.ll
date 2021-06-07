@.str.0 = private unnamed_addr constant [11 x i8] c"%d; %d; %d\00", align 1
declare dso_local i32 @printf(i8*, ...)

define dso_local i32 @main() {
  %1 = alloca i32, align 4
  %2 = alloca i32*, align 4
  %3 = alloca i32**, align 4
  %4 = alloca i32, align 4
  store i32 10, i32* %1, align 4
  store i32* %1, i32** %2, align 4
  store i32** %2, i32*** %3, align 4
  %5 = load i32, i32* %1, align 4
  %6 = load i32*, i32** %2, align 4
  %7 = load i32, i32* %6, align 4
  %8 = load i32**, i32*** %3, align 4
  %9 = load i32*, i32** %8, align 4
  %10 = load i32, i32* %9, align 4
  %11 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.str.0, i64 0, i64 0), i32 %5, i32 %7, i32 %10)
  ret i32 1

12:
  %13 = load i32, i32* %4, align 4
  ret i32 %13

}
