@.str.0 = private unnamed_addr constant [5 x i8] c"%d; \00", align 1
@.str.1 = private unnamed_addr constant [5 x i8] c"%d; \00", align 1
@.str.2 = private unnamed_addr constant [5 x i8] c"%d; \00", align 1
@.str.3 = private unnamed_addr constant [5 x i8] c"%d; \00", align 1
declare dso_local i32 @printf(i8*, ...)

define dso_local i32 @main() {
  %1 = alloca i32, align 4
  %2 = add nsw i32 2, 3
  %3 = mul nsw i32 2, %2
  %4 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.0, i64 0, i64 0), i32 %3)
  %5 = mul nsw i32 2, 4
  %6 = add nsw i32 %5, 2
  %7 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.1, i64 0, i64 0), i32 %6)
  %8 = sdiv i32 10, 2
  %9 = sdiv i32 10, 2
  %10 = add nsw i32 %8, %9
  %11 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.2, i64 0, i64 0), i32 %10)
  %12 = sub nsw i32 100, 80
  %13 = sdiv i32 %12, 2
  %14 = sub nsw i32 5, 5
  %15 = add nsw i32 %13, %14
  %16 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.3, i64 0, i64 0), i32 %15)
  ret i32 1

17:
  %18 = load i32, i32* %1, align 4
  ret i32 %18

}
