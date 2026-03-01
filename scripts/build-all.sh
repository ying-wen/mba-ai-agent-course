#!/bin/bash
# MBA Agent Course - 全格式编译脚本
# 将 slides/*.md 和 lecture-notes/*.md 编译为 PDF/HTML/PPTX
# 用法: ./scripts/build-all.sh [--watch]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PROJECT_DIR/all-pdf"
HTML_DIR="$PROJECT_DIR/all-html"
PPTX_DIR="$PROJECT_DIR/all-pptx"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查依赖
check_deps() {
    local missing=()
    command -v marp >/dev/null 2>&1 || missing+=("marp")
    command -v pandoc >/dev/null 2>&1 || missing+=("pandoc")
    
    if [ ${#missing[@]} -gt 0 ]; then
        log_error "缺少依赖: ${missing[*]}"
        log_info "安装命令: npm install -g @marp-team/marp-cli && brew install pandoc"
        exit 1
    fi
}

# 创建输出目录
setup_dirs() {
    mkdir -p "$OUTPUT_DIR" "$HTML_DIR" "$PPTX_DIR"
}

# 编译 Marp slides (带 marp: true 的 md 文件)
compile_marp_slides() {
    log_info "编译 Marp Slides..."
    local count=0
    
    for md in "$PROJECT_DIR"/slides/*.md "$PROJECT_DIR"/slides-marp/*.md; do
        [ -f "$md" ] || continue
        
        # 检查是否是 marp 格式
        if head -20 "$md" | grep -q "marp: true"; then
            local basename=$(basename "$md" .md)
            
            # PDF
            marp "$md" --pdf --allow-local-files -o "$OUTPUT_DIR/${basename}.pdf" 2>/dev/null && \
                log_info "  ✓ PDF: ${basename}.pdf" || log_warn "  ✗ PDF失败: $basename"
            
            # HTML
            marp "$md" --html --allow-local-files -o "$HTML_DIR/${basename}.html" 2>/dev/null && \
                log_info "  ✓ HTML: ${basename}.html" || log_warn "  ✗ HTML失败: $basename"
            
            # PPTX
            marp "$md" --pptx --allow-local-files -o "$PPTX_DIR/${basename}.pptx" 2>/dev/null && \
                log_info "  ✓ PPTX: ${basename}.pptx" || log_warn "  ✗ PPTX失败: $basename"
            
            ((count++))
        fi
    done
    
    log_info "Marp slides 编译完成: $count 个文件"
}

# 编译普通 Markdown (lecture-notes, assignments 等)
compile_markdown() {
    log_info "编译 Markdown 文档..."
    local count=0
    
    # Lecture notes
    for md in "$PROJECT_DIR"/lecture-notes/*.md; do
        [ -f "$md" ] || continue
        [[ "$(basename "$md")" == "README.md" ]] && continue
        
        local basename=$(basename "$md" .md)
        
        # PDF via pandoc
        pandoc "$md" -o "$OUTPUT_DIR/${basename}.pdf" \
            --pdf-engine=wkhtmltopdf \
            -V geometry:margin=1in \
            -V fontsize=11pt \
            --highlight-style=tango 2>/dev/null || \
        pandoc "$md" -o "$OUTPUT_DIR/${basename}.pdf" \
            -t html5 --embed-resources --standalone 2>/dev/null && \
            log_info "  ✓ PDF: ${basename}.pdf" || log_warn "  ✗ PDF失败: $basename (尝试HTML转换)"
        
        # HTML
        pandoc "$md" -o "$HTML_DIR/${basename}.html" \
            --standalone --embed-resources \
            --highlight-style=tango \
            --metadata title="$basename" 2>/dev/null && \
            log_info "  ✓ HTML: ${basename}.html" || log_warn "  ✗ HTML失败: $basename"
        
        ((count++))
    done
    
    # Assignments
    for md in "$PROJECT_DIR"/assignments/*.md; do
        [ -f "$md" ] || continue
        local basename="assignments-$(basename "$md" .md)"
        
        pandoc "$md" -o "$OUTPUT_DIR/${basename}.pdf" \
            --standalone --embed-resources 2>/dev/null && \
            log_info "  ✓ PDF: ${basename}.pdf"
        
        pandoc "$md" -o "$HTML_DIR/${basename}.html" \
            --standalone --embed-resources 2>/dev/null && \
            log_info "  ✓ HTML: ${basename}.html"
        
        ((count++))
    done
    
    # Code labs README
    for lab in "$PROJECT_DIR"/code-labs/*/; do
        [ -d "$lab" ] || continue
        local readme="$lab/README.md"
        [ -f "$readme" ] || continue
        
        local labname=$(basename "$lab")
        
        pandoc "$readme" -o "$OUTPUT_DIR/${labname}.pdf" \
            --standalone --embed-resources 2>/dev/null && \
            log_info "  ✓ PDF: ${labname}.pdf"
        
        pandoc "$readme" -o "$HTML_DIR/${labname}.html" \
            --standalone --embed-resources 2>/dev/null && \
            log_info "  ✓ HTML: ${labname}.html"
        
        ((count++))
    done
    
    # Root docs
    for md in "$PROJECT_DIR"/*.md; do
        [ -f "$md" ] || continue
        local basename=$(basename "$md" .md)
        [[ "$basename" == "README" || "$basename" == "SYNC-CHECKLIST" || "$basename" == "IMPROVEMENT-PLAN" ]] && continue
        
        pandoc "$md" -o "$OUTPUT_DIR/${basename}.pdf" \
            --standalone --embed-resources 2>/dev/null && \
            log_info "  ✓ PDF: ${basename}.pdf"
        
        pandoc "$md" -o "$HTML_DIR/${basename}.html" \
            --standalone --embed-resources 2>/dev/null && \
            log_info "  ✓ HTML: ${basename}.html"
        
        ((count++))
    done
    
    log_info "Markdown 文档编译完成: $count 个文件"
}

# 生成索引
generate_index() {
    log_info "生成文件索引..."
    
    cat > "$OUTPUT_DIR/README.md" << 'EOF'
# MBA Agent Course - PDF 文件索引

自动生成时间: $(date '+%Y-%m-%d %H:%M:%S')

## 📚 Lecture Notes
EOF
    
    ls -1 "$OUTPUT_DIR"/L*.pdf 2>/dev/null | while read f; do
        echo "- [$(basename "$f")]($(basename "$f"))" >> "$OUTPUT_DIR/README.md"
    done
    
    cat >> "$OUTPUT_DIR/README.md" << 'EOF'

## 🎬 Slides
EOF
    
    ls -1 "$OUTPUT_DIR"/day*.pdf 2>/dev/null | while read f; do
        echo "- [$(basename "$f")]($(basename "$f"))" >> "$OUTPUT_DIR/README.md"
    done
    
    cat >> "$OUTPUT_DIR/README.md" << 'EOF'

## 📝 其他
EOF
    
    ls -1 "$OUTPUT_DIR"/*.pdf 2>/dev/null | grep -v "^L" | grep -v "^day" | while read f; do
        echo "- [$(basename "$f")]($(basename "$f"))" >> "$OUTPUT_DIR/README.md"
    done
    
    log_info "索引已生成: $OUTPUT_DIR/README.md"
}

# 统计
print_stats() {
    echo ""
    echo "=========================================="
    echo "编译完成统计"
    echo "=========================================="
    echo "PDF:  $(ls -1 "$OUTPUT_DIR"/*.pdf 2>/dev/null | wc -l | tr -d ' ') 个文件"
    echo "HTML: $(ls -1 "$HTML_DIR"/*.html 2>/dev/null | wc -l | tr -d ' ') 个文件"
    echo "PPTX: $(ls -1 "$PPTX_DIR"/*.pptx 2>/dev/null | wc -l | tr -d ' ') 个文件"
    echo ""
    echo "输出目录:"
    echo "  PDF:  $OUTPUT_DIR"
    echo "  HTML: $HTML_DIR"
    echo "  PPTX: $PPTX_DIR"
    echo "=========================================="
}

# Watch 模式
watch_mode() {
    log_info "进入 Watch 模式... (Ctrl+C 退出)"
    
    if command -v fswatch >/dev/null 2>&1; then
        fswatch -o "$PROJECT_DIR"/slides/*.md \
                   "$PROJECT_DIR"/lecture-notes/*.md \
                   "$PROJECT_DIR"/assignments/*.md | while read; do
            log_info "检测到文件变更，重新编译..."
            main_build
        done
    else
        log_warn "fswatch 未安装，使用轮询模式 (每60秒检查)"
        while true; do
            sleep 60
            log_info "定时检查..."
            main_build
        done
    fi
}

# 主构建流程
main_build() {
    check_deps
    setup_dirs
    compile_marp_slides
    compile_markdown
    generate_index
    print_stats
}

# 入口
case "${1:-}" in
    --watch|-w)
        main_build
        watch_mode
        ;;
    --help|-h)
        echo "用法: $0 [选项]"
        echo ""
        echo "选项:"
        echo "  --watch, -w    监听文件变更自动重编译"
        echo "  --help, -h     显示帮助"
        echo ""
        echo "输出目录:"
        echo "  all-pdf/   - PDF 文件"
        echo "  all-html/  - HTML 文件"
        echo "  all-pptx/  - PowerPoint 文件"
        ;;
    *)
        main_build
        ;;
esac
