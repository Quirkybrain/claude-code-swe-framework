import assert from 'node:assert/strict'
import { spawn } from 'node:child_process'
import { Readable } from 'node:stream'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import test from 'node:test'
import plugin from '../.opencode/plugins/swe-guards.js'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')

globalThis.Bun = {
  spawn(command, options) {
    const child = spawn(command[0], command.slice(1), {
      cwd: options.cwd,
      stdio: ['pipe', 'ignore', 'pipe'],
    })
    options.stdin.text().then((payload) => child.stdin.end(payload))
    return {
      exited: new Promise((resolve) => child.on('exit', resolve)),
      stderr: Readable.toWeb(child.stderr),
    }
  },
}

let before
await plugin.setup({
  location: { project: { canonical: root } },
  tool: { async hook(name, handler) {
    assert.equal(name, 'execute.before')
    before = handler
  } },
})

test('specialist dispatch requires a frozen handoff', async () => {
  await assert.rejects(
    before({ tool: 'subagent', input: { agent: 'implementation-engineer', prompt: 'Implement feature' } }),
    /HANDOFF:/,
  )
})

test('artifact writes require Producer metadata', async () => {
  await assert.rejects(
    before({ tool: 'write', input: { filePath: 'artifacts/adapter-test.md', content: '# Test' } }),
    /Producer/,
  )
})

test('apply_patch checks every changed path', async () => {
  const original = globalThis.Bun.spawn
  const calls = []
  globalThis.Bun.spawn = (command, options) => {
    calls.push({ command, input: options.stdin })
    return { exited: Promise.resolve(0), stderr: new Blob([]) }
  }
  try {
    await before({
      tool: 'apply_patch',
      input: { patchText: '*** Begin Patch\n*** Update File: input/old.md\n*** Move to: input/new.md\n*** End Patch' },
    })
    assert.equal(calls.length, 2)
    const targets = await Promise.all(calls.map(async (call) => JSON.parse(await call.input.text()).tool_input.file_path))
    assert.deepEqual(targets, ['input/old.md', 'input/new.md'])
  } finally {
    globalThis.Bun.spawn = original
  }
})
