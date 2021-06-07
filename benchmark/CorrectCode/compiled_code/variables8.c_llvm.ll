@.str.0 = private unnamed_addr constant [5 x i8] c"%d; \00", align 1
declare dso_local i32 @printf(i8*, ...)

define dso_local i32 @main() {
  %1 = alloca [3 x i32], align 4
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  %4 = getelementptr inbounds [3 x i32], [3 x i32]* %1, i64 0, i64 0
  store i32 10, i32* %4, align 4
  %5 = getelementptr inbounds [3 x i32], [3 x i32]* %1, i64 0, i64 1
  store i32 20, i32* %5, align 4
  %6 = getelementptr inbounds [3 x i32], [3 x i32]* %1, i64 0, i64 2
  store i32 30, i32* %6, align 4
  store i32 1, i32* %2, align 4
  br label %7

7:
  %8 = load i32, i32* %2, align 4
  %9 = icmp slt i32 %8, 4
  br i1 %9, label %10, label %19

10:
  %11 = load i32, i32* %2, align 4
  %12 = sub nsw i32 %11, 1
  %13 = sext i32 %12 to i64
  %14 = getelementptr inbounds [3 x i32], [3 x i32]* %1, i64 0, i64 %13
  %15 = load i32, i32* %14, align 4
  %16 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.0, i64 0, i64 0), i32 %15)
  %17 = load i32, i32* %2, align 4
  %18 = add nsw i32 %17, 1
  store i32 %18, i32* %2, align 4
  br label %7

19:
  ret i32 1

20:
  %21 = load i32, i32* %3, align 4
  ret i32 %21

}
