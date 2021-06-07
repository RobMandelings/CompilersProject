@.str.0 = private unnamed_addr constant [7 x i8] c"%d%f%c\00", align 1
declare dso_local i32 @printf(i8*, ...)

define dso_local i32 @main() {
  %1 = alloca i32, align 4
  %2 = fpext float 0.5 to double
  %3 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str.0, i64 0, i64 0), i32 10, double %2, i8 37)
  %4 = load i32, i32* %1, align 4
  ret i32 %4

}
