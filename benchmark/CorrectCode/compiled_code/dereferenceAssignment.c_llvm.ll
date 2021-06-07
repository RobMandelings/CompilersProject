@.str.0 = private unnamed_addr constant [5 x i8] c"%d; \00", align 1
@.str.1 = private unnamed_addr constant [5 x i8] c"%d\n\00", align 1
@.str.2 = private unnamed_addr constant [5 x i8] c"%d; \00", align 1
@.str.3 = private unnamed_addr constant [5 x i8] c"%d\n\00", align 1
declare dso_local i32 @printf(i8*, ...)

define dso_local i32 @main() {
  %1 = alloca i32, align 4
  %2 = alloca i32*, align 4
  %3 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  store i32* %1, i32** %2, align 4
  %4 = load i32*, i32** %2, align 4
  store i32 10, i32* %4, align 4
  %5 = load i32, i32* %1, align 4
  %6 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.0, i64 0, i64 0), i32 %5)
  %7 = load i32*, i32** %2, align 4
  %8 = load i32, i32* %7, align 4
  %9 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.1, i64 0, i64 0), i32 %8)
  %10 = load i32*, i32** %2, align 4
  %11 = load i32*, i32** %2, align 4
  %12 = load i32, i32* %11, align 4
  %13 = add nsw i32 %12, 1
  store i32 %13, i32* %10, align 4
  %14 = load i32, i32* %1, align 4
  %15 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.2, i64 0, i64 0), i32 %14)
  %16 = load i32*, i32** %2, align 4
  %17 = load i32, i32* %16, align 4
  %18 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.3, i64 0, i64 0), i32 %17)
  ret i32 1

19:
  %20 = load i32, i32* %3, align 4
  ret i32 %20

}
