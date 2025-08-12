-- WezTerm configuration
-- Migrated from iTerm2 settings

local wezterm = require 'wezterm'
local config = wezterm.config_builder()

-- Font configuration
config.font = wezterm.font('MesloLGS Nerd Font', {weight='Regular', stretch='Normal', style='Normal'})
config.font_size = 12.0
config.line_height = 1.0

-- Color scheme (dark theme matching iTerm2 settings)
config.colors = {
  -- Foreground and background
  foreground = '#a0a0a0',  -- ~62.7% gray from iTerm2
  background = '#121212',  -- ~7% gray from iTerm2
  
  -- Cursor colors
  cursor_bg = '#bbbbbb',   -- ~73.3% gray
  cursor_fg = '#ffffff',
  cursor_border = '#bbbbbb',
  
  -- Selection colors
  selection_fg = '#bbbcc0', -- ~71-75% gray blend
  selection_bg = '#453a39', -- ~27% gray with slight warmth
  
  -- ANSI colors (converted from iTerm2)
  ansi = {
    '#1b1d1e',  -- black (Ansi 0)
    '#f92672',  -- red (Ansi 1)
    '#a6e22e',  -- green (Ansi 2)
    '#fd971f',  -- yellow (Ansi 3)
    '#66d9ef',  -- blue (Ansi 4)
    '#9e6ffe',  -- magenta (Ansi 5)
    '#5e7175',  -- cyan (Ansi 6)
    '#ccccc6',  -- white (Ansi 7)
  },
  
  -- Bright ANSI colors
  brights = {
    '#505354',  -- bright black (Ansi 8)
    '#ff669d',  -- bright red (Ansi 9)
    '#beed5f',  -- bright green (Ansi 10)
    '#e6db74',  -- bright yellow (Ansi 11)
    '#66d9ef',  -- bright blue (Ansi 12)
    '#9e6ffe',  -- bright magenta (Ansi 13)
    '#a3babf',  -- bright cyan (Ansi 14)
    '#f8f8f2',  -- bright white (Ansi 15)
  },
}

-- Window configuration
config.initial_cols = 80
config.initial_rows = 25
config.window_padding = {
  left = 2,
  right = 2,
  top = 2,
  bottom = 2,
}

-- Yabai compatibility
config.window_decorations = "RESIZE"  -- Keeps resize handle for proper tiling
config.use_resize_increments = true   -- Better grid snapping

-- Features
config.enable_scroll_bar = false
config.scrollback_lines = 1000
config.audible_bell = 'Disabled'  -- iTerm2 had "Silence Bell" = true

-- Tab bar (keeping it minimal like the terminal-first approach)
config.hide_tab_bar_if_only_one_tab = true
config.tab_bar_at_bottom = false
config.use_fancy_tab_bar = false

-- Leader key configuration (like tmux)
config.leader = { key = 'a', mods = 'CTRL', timeout_milliseconds = 1000 }

-- Key bindings to match iTerm2 keyboard map + multiplexing
config.keys = {
  -- Option+Backspace to delete word
  {
    key = 'Backspace',
    mods = 'OPT',
    action = wezterm.action.SendString '\x1b\x7f',
  },
  -- Cmd+Left to move to beginning of line
  {
    key = 'LeftArrow',
    mods = 'CMD',
    action = wezterm.action.SendString '\x01',
  },
  -- Cmd+Right to move to end of line  
  {
    key = 'RightArrow',
    mods = 'CMD',
    action = wezterm.action.SendString '\x05',
  },
  -- Option+Left to move word left
  {
    key = 'LeftArrow',
    mods = 'OPT',
    action = wezterm.action.SendString '\x1bb',
  },
  -- Option+Right to move word right
  {
    key = 'RightArrow',
    mods = 'OPT',
    action = wezterm.action.SendString '\x1bf',
  },
  -- Cmd+Backspace to delete to beginning of line
  {
    key = 'Backspace',
    mods = 'CMD',
    action = wezterm.action.SendString '\x15',
  },
  -- Delete key sends forward delete
  {
    key = 'Delete',
    mods = 'NONE',
    action = wezterm.action.SendString '\x04',
  },
  
  -- Pane splitting (using leader key)
  {
    key = '|',
    mods = 'LEADER|SHIFT',
    action = wezterm.action.SplitHorizontal { domain = 'CurrentPaneDomain' },
  },
  {
    key = '-',
    mods = 'LEADER',
    action = wezterm.action.SplitVertical { domain = 'CurrentPaneDomain' },
  },
  
  -- Pane navigation
  {
    key = 'h',
    mods = 'LEADER',
    action = wezterm.action.ActivatePaneDirection 'Left',
  },
  {
    key = 'l',
    mods = 'LEADER',
    action = wezterm.action.ActivatePaneDirection 'Right',
  },
  {
    key = 'k',
    mods = 'LEADER',
    action = wezterm.action.ActivatePaneDirection 'Up',
  },
  {
    key = 'j',
    mods = 'LEADER',
    action = wezterm.action.ActivatePaneDirection 'Down',
  },
  
  -- Pane resizing
  {
    key = 'H',
    mods = 'LEADER|SHIFT',
    action = wezterm.action.AdjustPaneSize { 'Left', 5 },
  },
  {
    key = 'L',
    mods = 'LEADER|SHIFT',
    action = wezterm.action.AdjustPaneSize { 'Right', 5 },
  },
  {
    key = 'K',
    mods = 'LEADER|SHIFT',
    action = wezterm.action.AdjustPaneSize { 'Up', 5 },
  },
  {
    key = 'J',
    mods = 'LEADER|SHIFT',
    action = wezterm.action.AdjustPaneSize { 'Down', 5 },
  },
  
  -- Close pane
  {
    key = 'x',
    mods = 'LEADER',
    action = wezterm.action.CloseCurrentPane { confirm = true },
  },
  
  -- Toggle pane zoom
  {
    key = 'z',
    mods = 'LEADER',
    action = wezterm.action.TogglePaneZoomState,
  },
  
  -- Show debug overlay (see all keys being pressed)
  {
    key = 'd',
    mods = 'LEADER',
    action = wezterm.action.ShowDebugOverlay,
  },
  
  -- Open documentation browser in glow
  {
    key = 'D',
    mods = 'LEADER|SHIFT',
    action = wezterm.action.SplitPane {
      direction = 'Right',
      size = { Percent = 60 },
      command = { args = { '/opt/homebrew/bin/glow', os.getenv('HOME') .. '/.docs/' } },
    },
  },
  
  -- Launch 4-tile development workspace
  {
    key = 'w',
    mods = 'LEADER',
    action = wezterm.action_callback(function(window, pane)
      -- Split right for btop (50/50)
      window:perform_action(
        wezterm.action.SplitPane {
          direction = 'Right',
          command = { args = { '/opt/homebrew/bin/btop' } },
        },
        pane
      )
      
      -- Go back to left pane
      window:perform_action(wezterm.action.ActivatePaneDirection 'Left', pane)
      
      -- Split bottom for lazygit
      window:perform_action(
        wezterm.action.SplitPane {
          direction = 'Down',
          command = { args = { '/opt/homebrew/bin/lazygit' } },
        },
        pane
      )
      
      -- Go to top-right and split for fourth pane
      window:perform_action(wezterm.action.ActivatePaneDirection 'Right', pane)
      window:perform_action(wezterm.action.ActivatePaneDirection 'Up', pane)
      window:perform_action(
        wezterm.action.SplitPane {
          direction = 'Down',
        },
        pane
      )
      
      -- Return to top-left (main workspace)
      window:perform_action(wezterm.action.ActivatePaneDirection 'Left', pane)
      window:perform_action(wezterm.action.ActivatePaneDirection 'Up', pane)
    end),
  },
  
  -- Option+Delete to delete word forward
  {
    key = 'Delete',
    mods = 'OPT',
    action = wezterm.action.SendString '\x1bd',
  },
  
  -- === Workspace Launchers ===
  
  -- Home Command Center (dotfiles management)
  {
    key = 'h',
    mods = 'LEADER',
    action = wezterm.action.SpawnCommandInNewWindow {
      args = { '/Users/nehalecky/.local/bin/workspace-home' },
    },
  },
  
  -- Project Development Workspace
  {
    key = 'W',
    mods = 'LEADER|SHIFT',
    action = wezterm.action.SpawnCommandInNewWindow {
      args = { '/Users/nehalecky/.local/bin/workspace-dev' },
    },
  },
  
  -- Refresh workspace-home 
  {
    key = 'r',
    mods = 'LEADER',
    action = wezterm.action.SpawnCommandInNewTab {
      args = { '/Users/nehalecky/.local/bin/workspace-refresh' },
    },
  },
  
  -- === Modern TUI Tools (Phase 1 Aggressive) ===
  
  -- File Management
  {
    key = 'f',
    mods = 'LEADER',
    action = wezterm.action.SpawnCommandInNewTab {
      args = { '/opt/homebrew/bin/yazi' },
      cwd = wezterm.home_dir,
    },
  },
  
  -- Text Editor (Helix)
  {
    key = 'e',
    mods = 'LEADER',
    action = wezterm.action.SpawnCommandInNewTab {
      args = { '/opt/homebrew/bin/hx', '.' },
    },
  },
  
  -- Git Management (lazygit already mapped, adding to new tab)
  {
    key = 'g',
    mods = 'LEADER',
    action = wezterm.action.SpawnCommandInNewTab {
      args = { '/opt/homebrew/bin/lazygit' },
    },
  },
  
  -- Docker Management
  {
    key = 'D',
    mods = 'LEADER',
    action = wezterm.action.SpawnCommandInNewTab {
      args = { '/opt/homebrew/bin/lazydocker' },
    },
  },
  
  -- Kubernetes Management
  {
    key = 'k',
    mods = 'LEADER',
    action = wezterm.action.SpawnCommandInNewTab {
      args = { '/opt/homebrew/bin/k9s' },
    },
  },
  
  -- API Testing
  {
    key = 'a',
    mods = 'LEADER',
    action = wezterm.action.SpawnCommandInNewTab {
      args = { '/opt/homebrew/bin/atac' },
    },
  },
  
  -- System Process Monitor (modern procs)
  {
    key = 'p',
    mods = 'LEADER',
    action = wezterm.action.SpawnCommandInNewTab {
      args = { '/opt/homebrew/bin/procs' },
    },
  },
  
  -- System Monitor (btop)
  {
    key = 'm',
    mods = 'LEADER',
    action = wezterm.action.SpawnCommandInNewTab {
      args = { '/opt/homebrew/bin/btop' },
    },
  },
  
  -- System Monitor btop (uppercase for new window)
  {
    key = 'M',
    mods = 'LEADER',
    action = wezterm.action.SpawnCommandInNewWindow {
      args = { '/opt/homebrew/bin/btop' },
    },
  },
  
  -- Network Monitor
  {
    key = 'n',
    mods = 'LEADER',
    action = wezterm.action.SpawnCommandInNewTab {
      args = { '/opt/homebrew/bin/bandwhich' },
    },
  },
  
  -- Disk Usage Analyzer
  {
    key = 'u',
    mods = 'LEADER',
    action = wezterm.action.SpawnCommandInNewTab {
      args = { '/opt/homebrew/bin/dust' },
    },
  },
  
  -- Modern Session Manager (Zellij)
  {
    key = 's',
    mods = 'LEADER',
    action = wezterm.action.SpawnCommandInNewTab {
      args = { '/opt/homebrew/bin/zellij' },
    },
  },
}

-- Mouse configuration
config.mouse_bindings = {
  -- Right click to paste
  {
    event = { Down = { streak = 1, button = 'Right' } },
    mods = 'NONE',
    action = wezterm.action.PasteFrom 'Clipboard',
  },
}

-- Working directory
config.default_cwd = wezterm.home_dir

-- Set PATH to include Homebrew (for macOS)
config.set_environment_variables = {
  PATH = '/opt/homebrew/bin:/usr/local/bin:' .. os.getenv('PATH'),
}

-- Performance
config.front_end = 'WebGpu'  -- GPU acceleration
config.max_fps = 120

-- Enable ligatures (iTerm2 had "ASCII Ligatures" = true)
config.harfbuzz_features = { 'calt=1', 'clig=1', 'liga=1' }

-- macOS specific
config.native_macos_fullscreen_mode = true
config.macos_window_background_blur = 0  -- No blur by default

-- Hyperlink configuration (iTerm2 had link color configured)
config.hyperlink_rules = wezterm.default_hyperlink_rules()

-- Add markdown file link handler
table.insert(config.hyperlink_rules, {
  regex = '\\[([^\\]]+)\\]\\(([^\\)]+\\.md)\\)',
  format = 'file://$2',
  highlight = 1,
})

-- Make .md files clickable when they appear as plain text
table.insert(config.hyperlink_rules, {
  regex = '(\\S+\\.md)',
  format = 'file://$1',
  highlight = 0,
})

-- Status bar configuration
config.status_update_interval = 1000
config.enable_tab_bar = true
config.tab_bar_at_bottom = true
config.show_tab_index_in_tab_bar = false
config.show_tabs_in_tab_bar = true
config.hide_tab_bar_if_only_one_tab = false

-- Event handler for status bar
wezterm.on('update-status', function(window, pane)
  -- Get current working directory
  local cwd = pane:get_current_working_dir()
  if cwd then
    cwd = cwd.file_path
    -- Shorten home directory
    cwd = cwd:gsub(os.getenv('HOME'), '~')
  else
    cwd = '~'
  end
  
  -- Left status (workspace/cwd)
  window:set_left_status(wezterm.format {
    { Foreground = { Color = '#66d9ef' } },
    { Text = '  ' .. cwd .. ' ' },
  })
  
  -- Get the active key table name
  local key_table = window:active_key_table()
  
  -- Right status (leader key indicator and key sequence)
  local leader = ''
  local key_status = ''
  
  if window:leader_is_active() then
    leader = '  LEADER  '
  end
  
  if key_table then
    key_status = ' [' .. key_table .. '] '
  end
  
  window:set_right_status(wezterm.format {
    { Foreground = { Color = '#f92672' } },
    { Text = leader },
    { Foreground = { Color = '#a6e22e' } },
    { Text = key_status },
  })
end)

return config