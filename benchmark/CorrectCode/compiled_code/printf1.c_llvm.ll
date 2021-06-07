@.str.0 = private unnamed_addr constant [15 x i8] c"Hello World!\n\00", align 1
declare dso_local i32 @printf(i8*, ...)

define dso_local i32 @main() {
  %1 = alloca i32, align 4
  %2 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([15 x i8], [15 x i8]* @.str.0, i64 0, i64 0))
  %3 = load i32, i32* %1, align 4
  ret i32 %3

}
