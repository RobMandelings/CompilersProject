@.str.0 = private unnamed_addr constant [4 x i8] c"%d;\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d;\00", align 1
@.str.2 = private unnamed_addr constant [4 x i8] c"%d;\00", align 1
@.str.3 = private unnamed_addr constant [4 x i8] c"%d;\00", align 1
declare dso_local i32 @printf(i8*, ...)
@x = dso_local global i32 10, align 4

define dso_local i32 @main() {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = load i32, i32* @x, align 4
  %5 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.0, i64 0, i64 0), i32 %4)
  store i32 20, i32* %1, align 4
  %6 = load i32, i32* %1, align 4
  %7 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %6)
  store i32 30, i32* %1, align 4
  br label %8

8:
  %9 = icmp ne i32 1, 0
  br i1 %9, label %10, label %15

10:
  %11 = load i32, i32* %1, align 4
  %12 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.2, i64 0, i64 0), i32 %11)
  store i32 40, i32* %2, align 4
  %13 = load i32, i32* %2, align 4
  %14 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.3, i64 0, i64 0), i32 %13)
  br label %15

15:
  ret i32 1

16:
  %17 = load i32, i32* %3, align 4
  ret i32 %17

}
