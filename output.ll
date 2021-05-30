; ModuleID = 'testinput/output.ll'
source_filename = "testinput/output.ll"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str.0 = private unnamed_addr constant [31 x i8] c"Hi, and welcome to my guide %d\00", align 1
@.str.1 = private unnamed_addr constant [3 x i8] c"%d\00", align 1

declare dso_local i32 @__isoc99_scanf(i8*, ...)

declare dso_local i32 @printf(i8*, ...)

define dso_local i32 @main() {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  store i32 10, i32* %1, align 4
  %3 = call i32 (i8*, ...) @__isoc99_scanf(i8* getelementptr inbounds ([31 x i8], [31 x i8]* @.str.0, i64 0, i64 0), i32* %1)
  %4 = load i32, i32* %1, align 4
  %5 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str.1, i64 0, i64 0), i32 %4)
  %6 = load i32, i32* %2, align 4
  ret i32 %6
}
