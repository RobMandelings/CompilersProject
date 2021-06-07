@.str.0 = private unnamed_addr constant [7 x i8] c"Hello \00", align 1
@.str.1 = private unnamed_addr constant [8 x i8] c"World\n\00", align 1
@.str.2 = private unnamed_addr constant [8 x i8] c"World\n\00", align 1
declare dso_local i32 @printf(i8*, ...)

define dso_local void @f() {
  %1 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str.0, i64 0, i64 0))
  ret void

2:
  ret void

}
define dso_local void @g() {
  %1 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([8 x i8], [8 x i8]* @.str.1, i64 0, i64 0))
  call void @f()
  %2 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([8 x i8], [8 x i8]* @.str.2, i64 0, i64 0))
  ret void

}
define dso_local i32 @main() {
  %1 = alloca i32, align 4
  call void @f()
  call void @g()
  ret i32 1

2:
  %3 = load i32, i32* %1, align 4
  ret i32 %3

}
