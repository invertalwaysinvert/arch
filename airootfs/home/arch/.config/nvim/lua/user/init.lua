vim.opt.keymap = "dvorak"
vim.opt.background = "dark"
vim.opt.viminfo = { "'100" }

return {
  colorscheme = "tokyonight-storm",
  plugins = {
    "ThePrimeagen/harpoon",
    { "mbbill/undotree", lazy = false },
    {
      "catppuccin/nvim",
      as = "catppuccin",
      lazy = false,
      config = function() require("catppuccin").setup {} end,
    },
    {
      "nvim-treesitter/nvim-treesitter",
      dependencies = { "windwp/nvim-ts-autotag", "JoosepAlviste/nvim-ts-context-commentstring" },
      event = "User AstroFile",
      cmd = {
        "TSBufDisable",
        "TSBufEnable",
        "TSBufToggle",
        "TSDisable",
        "TSEnable",
        "TSToggle",
        "TSInstall",
        "TSInstallInfo",
        "TSInstallSync",
        "TSModuleInfo",
        "TSUninstall",
        "TSUpdate",
        "TSUpdateSync",
      },
      build = ":TSUpdate",
      opts = {
        ensure_installed = { "python", "javascript", "typescript", "rust", "lua", "vim", "vimdoc", "query" },
        sync_install = false,
        auto_install = true,
        highlight = { enable = true, additional_vim_regex_highlighting = false },
        incremental_selection = { enable = true },
        indent = { enable = true },
        autotag = { enable = true },
        context_commentstring = { enable = true, enable_autocmd = false },
      },
      config = require "plugins.configs.nvim-treesitter",
    },
    "nvim-treesitter/playground",
    "ggandor/leap.nvim",
    "tpope/vim-repeat",
    "ggandor/flit.nvim",
    { "projekt0n/github-nvim-theme", lazy = false },
    {
      "nyoom-engineering/oxocarbon.nvim",
      lazy = false,
    },
    {
      "folke/tokyonight.nvim",
      lazy = false,
      priority = 1000,
      opts = {},
    },
  },
}
