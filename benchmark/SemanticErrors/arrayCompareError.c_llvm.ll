
define dso_local i32 @main() {
  %1 = alloca [2 x i32], align 4
  %2 = alloca [2 x i32], align 4
  %3 = alloca i32, align 4
  ret i32 1

4:
  %5 = load i32, i32* %3, align 4
  ret i32 %5

}
