@.str.0 = private unnamed_addr constant [11 x i8] c"%d; %d; %d\00", align 1
declare dso_local i32 @printf(i8*, ...)

define dso_local i32 @main() {
  %1 = alloca [3 x i32], align 4
  %2 = alloca i32, align 4
  %3 = getelementptr inbounds [3 x i32], [3 x i32]* %1, i64 0, i64 0
  store i32 10, i32* %3, align 4
  %4 = getelementptr inbounds [3 x i32], [3 x i32]* %1, i64 0, i64 1
  store i32 20, i32* %4, align 4
  %5 = getelementptr inbounds [3 x i32], [3 x i32]* %1, i64 0, i64 2
  store i32 30, i32* %5, align 4
  %6 = getelementptr inbounds [3 x i32], [3 x i32]* %1, i64 0, i64 0
  %7 = load i32, i32* %6, align 4
  %8 = getelementptr inbounds [3 x i32], [3 x i32]* %1, i64 0, i64 1
  %9 = load i32, i32* %8, align 4
  %10 = getelementptr inbounds [3 x i32], [3 x i32]* %1, i64 0, i64 2
  %11 = load i32, i32* %10, align 4
  %12 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.str.0, i64 0, i64 0), i32 %7, i32 %9, i32 %11)
  %13 = load i32, i32* %2, align 4
  ret i32 %13

}
