return {
  "goolord/alpha-nvim",
  cmd = "Alpha",
  opts = function()
    local dashboard = require "alpha.themes.dashboard"
    dashboard.section.header.val = {
      " ⠀  ⠀   (\\__/)",
      "        (•ㅅ•)      Don’t talk to",
      "   __＿ノヽ ノ＼＿      me or my son",
      " `/　`/ ⌒Ｙ⌒ Ｙ    \\    ever again.",
      " ( 　(三ヽ人　 /　  |",
      " |　ﾉ⌒＼ ￣￣ヽ  _ノ",
      " ヽ＿＿＿＞､＿_／",
      "      ｜( 王 ﾉ〈  (\\__/)",
      "      / ﾐ`ー―彡\\  (•ㅅ•)",
      "     /  ╰    ╯  \\ /    \\>",
    }
    dashboard.section.header.opts.hl = "DashboardHeader"

    local button = require("astronvim.utils").alpha_button
    dashboard.section.buttons.val = {
      button("LDR n", "  New File  "),
      button("LDR f f", "  Find File  "),
      button("LDR f o", "  Recents  "),
      button("LDR f w", "  Find Word  "),
      button("LDR f '", "  Bookmarks  "),
      button("LDR S l", "  Last Session  "),
    }

    dashboard.config.layout[1].val = vim.fn.max { 2, vim.fn.floor(vim.fn.winheight(0) * 0.2) }
    dashboard.config.layout[3].val = 5
    dashboard.config.opts.noautocmd = true
    return dashboard
  end,
  config = require "plugins.configs.alpha",
}
