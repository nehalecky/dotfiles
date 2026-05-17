# autowt — automatic worktree shell integration
# Defines the shell function that lets autowt switch the *current* shell's
# directory. Binary managed by mise (github:irskep/autowt).
if command -v autowt &>/dev/null; then
    autowt() {
        local tmpfile exit_code
        tmpfile=$(mktemp)
        AUTOWT_SHELL_INTEGRATION_FILE="$tmpfile" command autowt "$@"
        exit_code=$?
        if [ -s "$tmpfile" ]; then
            eval "$(cat "$tmpfile")"
        fi
        rm -f "$tmpfile"
        return $exit_code
    }
    alias awt=autowt
fi
