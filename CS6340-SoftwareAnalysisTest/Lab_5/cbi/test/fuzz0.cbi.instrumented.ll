; ModuleID = 'fuzz0.instrumented.ll'
source_filename = "fuzz0.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

%struct._IO_FILE = type { i32, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, i8*, %struct._IO_marker*, %struct._IO_FILE*, i32, i32, i64, i16, i8, [1 x i8], i8*, i64, %struct._IO_codecvt*, %struct._IO_wide_data*, %struct._IO_FILE*, i8*, i64, i32, [20 x i8] }
%struct._IO_marker = type opaque
%struct._IO_codecvt = type opaque
%struct._IO_wide_data = type opaque

@stdin = external dso_local global %struct._IO_FILE*, align 8

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main() #0 !dbg !7 {
entry:
  %retval = alloca i32, align 4
  %input = alloca [65536 x i8], align 16
  %x = alloca i32, align 4
  %y = alloca i32, align 4
  %z = alloca i32, align 4
  store i32 0, i32* %retval, align 4
  tail call void @__coverage__(i32 27, i32 8)
  call void @llvm.dbg.declare(metadata [65536 x i8]* %input, metadata !11, metadata !DIExpression()), !dbg !16
  tail call void @__coverage__(i32 28, i32 9)
  %arraydecay = getelementptr inbounds [65536 x i8], [65536 x i8]* %input, i32 0, i32 0, !dbg !17
  tail call void @__coverage__(i32 28, i32 31)
  %0 = load %struct._IO_FILE*, %struct._IO_FILE** @stdin, align 8, !dbg !18
  tail call void @__coverage__(i32 28, i32 3)
  %call = call i8* @fgets(i8* %arraydecay, i32 65536, %struct._IO_FILE* %0), !dbg !19
  tail call void @__coverage__(i32 29, i32 7)
  call void @llvm.dbg.declare(metadata i32* %x, metadata !20, metadata !DIExpression()), !dbg !21
  tail call void @__coverage__(i32 29, i32 7)
  store i32 0, i32* %x, align 4, !dbg !21
  tail call void @__coverage__(i32 30, i32 7)
  call void @llvm.dbg.declare(metadata i32* %y, metadata !22, metadata !DIExpression()), !dbg !23
  tail call void @__coverage__(i32 30, i32 7)
  store i32 2, i32* %y, align 4, !dbg !23
  tail call void @__coverage__(i32 31, i32 7)
  call void @llvm.dbg.declare(metadata i32* %z, metadata !24, metadata !DIExpression()), !dbg !25
  tail call void @__coverage__(i32 31, i32 11)
  %1 = load i32, i32* %y, align 4, !dbg !26
  tail call void @__coverage__(i32 31, i32 15)
  %2 = load i32, i32* %x, align 4, !dbg !27
  tail call void @__dbz_sanitizer__(i32 %2, i32 31, i32 13)
  tail call void @__coverage__(i32 31, i32 13)
  %div = sdiv i32 %1, %2, !dbg !28
  tail call void @__coverage__(i32 31, i32 7)
  store i32 %div, i32* %z, align 4, !dbg !25
  tail call void @__coverage__(i32 32, i32 3)
  ret i32 0, !dbg !29
}

; Function Attrs: nounwind readnone speculatable
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

declare dso_local i8* @fgets(i8*, i32, %struct._IO_FILE*) #2

declare void @__coverage__(i32, i32)

declare void @__dbz_sanitizer__(i32, i32, i32)

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C99, file: !1, producer: "clang version 8.0.1-9 (tags/RELEASE_801/final)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !2, nameTableKind: None)
!1 = !DIFile(filename: "fuzz0.c", directory: "/home/cs6340/cbi/test")
!2 = !{}
!3 = !{i32 2, !"Dwarf Version", i32 4}
!4 = !{i32 2, !"Debug Info Version", i32 3}
!5 = !{i32 1, !"wchar_size", i32 4}
!6 = !{!"clang version 8.0.1-9 (tags/RELEASE_801/final)"}
!7 = distinct !DISubprogram(name: "main", scope: !1, file: !1, line: 26, type: !8, scopeLine: 26, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !2)
!8 = !DISubroutineType(types: !9)
!9 = !{!10}
!10 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!11 = !DILocalVariable(name: "input", scope: !7, file: !1, line: 27, type: !12)
!12 = !DICompositeType(tag: DW_TAG_array_type, baseType: !13, size: 524288, elements: !14)
!13 = !DIBasicType(name: "char", size: 8, encoding: DW_ATE_signed_char)
!14 = !{!15}
!15 = !DISubrange(count: 65536)
!16 = !DILocation(line: 27, column: 8, scope: !7)
!17 = !DILocation(line: 28, column: 9, scope: !7)
!18 = !DILocation(line: 28, column: 31, scope: !7)
!19 = !DILocation(line: 28, column: 3, scope: !7)
!20 = !DILocalVariable(name: "x", scope: !7, file: !1, line: 29, type: !10)
!21 = !DILocation(line: 29, column: 7, scope: !7)
!22 = !DILocalVariable(name: "y", scope: !7, file: !1, line: 30, type: !10)
!23 = !DILocation(line: 30, column: 7, scope: !7)
!24 = !DILocalVariable(name: "z", scope: !7, file: !1, line: 31, type: !10)
!25 = !DILocation(line: 31, column: 7, scope: !7)
!26 = !DILocation(line: 31, column: 11, scope: !7)
!27 = !DILocation(line: 31, column: 15, scope: !7)
!28 = !DILocation(line: 31, column: 13, scope: !7)
!29 = !DILocation(line: 32, column: 3, scope: !7)
