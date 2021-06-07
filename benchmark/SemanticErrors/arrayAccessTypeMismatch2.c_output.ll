
define dso_local i32 @main() {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  ret i32 0

3:
  %4 = load i32, i32* %2, align 4
  ret i32 %4

}
