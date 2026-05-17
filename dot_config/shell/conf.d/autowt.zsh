# autowt — automatic worktree shell integration
# Adds ~/bin to PATH (where autowt/awt binaries live) and defines the
# shell function that lets autowt switch the *current* shell's directory.
# Defined manually to avoid trap RETURN and broken completion output in rc3.
export PATH="$HOME/bin:$PATH"

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
