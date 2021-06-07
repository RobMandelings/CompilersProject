@.str.0 = private unnamed_addr constant [5 x i8] c"%d\n\00", align 1
declare dso_local i32 @printf(i8*, ...)

define dso_local i32 @main() {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  br label %3

3:
  %4 = load i32, i32* %1, align 4
  %5 = icmp slt i32 %4, 10
  br i1 %5, label %6, label %19

6:
  %7 = load i32, i32* %1, align 4
  %8 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.0, i64 0, i64 0), i32 %7)
  br label %9

9:
  %10 = load i32, i32* %1, align 4
  %11 = icmp eq i32 %10, 5
  br i1 %11, label %12, label %14

12:
  br label %19

13:
  br label %18

14:
  %15 = load i32, i32* %1, align 4
  %16 = add nsw i32 %15, 1
  store i32 %16, i32* %1, align 4
  br label %3

17:
  br label %18

18:
  store i32 10, i32* %1, align 4
  br label %3

19:
  ret i32 0

20:
  %21 = load i32, i32* %2, align 4
  ret i32 %21

}
