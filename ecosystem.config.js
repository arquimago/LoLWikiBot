module.exports = {
    apps: [
      {
        name: '@lolwbot',
        script: './lolwikibot.py',
        watch: true,
        kill_timeout: 1000,
        max_memory_restart: '100M',
        exec_interpreter: 'python3',
      },
    ],
  };