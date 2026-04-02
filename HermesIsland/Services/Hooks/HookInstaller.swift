//
//  HookInstaller.swift
//  HermesIsland
//
//  Installs the Hermes Island bridge plugin to ~/.hermes/plugins/
//

import Foundation

struct HookInstaller {

    /// Install the Hermes plugin on app launch
    static func installIfNeeded() {
        let hermesDir = FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent(".hermes")
        let pluginsDir = hermesDir.appendingPathComponent("plugins")
        let pluginDir = pluginsDir.appendingPathComponent("hermes_island")

        try? FileManager.default.createDirectory(
            at: pluginDir,
            withIntermediateDirectories: true
        )

        // Copy plugin files from app bundle
        let bundlePluginDir = Bundle.main.resourceURL?
            .appendingPathComponent("hermes-island-plugin")

        guard let source = bundlePluginDir, FileManager.default.fileExists(atPath: source.path) else {
            // Fallback: copy individual files
            copyBundledPlugin(to: pluginDir)
            return
        }

        // Copy all files from the bundled plugin directory
        if let files = try? FileManager.default.contentsOfDirectory(at: source, includingPropertiesForKeys: nil) {
            for file in files {
                let dest = pluginDir.appendingPathComponent(file.lastPathComponent)
                try? FileManager.default.removeItem(at: dest)
                try? FileManager.default.copyItem(at: file, to: dest)
            }
        }
    }

    private static func copyBundledPlugin(to pluginDir: URL) {
        // Copy __init__.py
        if let initPy = Bundle.main.url(forResource: "__init__", withExtension: "py") {
            let dest = pluginDir.appendingPathComponent("__init__.py")
            try? FileManager.default.removeItem(at: dest)
            try? FileManager.default.copyItem(at: initPy, to: dest)
        }

        // Copy plugin.yaml
        if let yaml = Bundle.main.url(forResource: "plugin", withExtension: "yaml") {
            let dest = pluginDir.appendingPathComponent("plugin.yaml")
            try? FileManager.default.removeItem(at: dest)
            try? FileManager.default.copyItem(at: yaml, to: dest)
        }
    }

    /// Check if plugin is installed
    static func isInstalled() -> Bool {
        let pluginDir = FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent(".hermes/plugins/hermes_island")
        let initFile = pluginDir.appendingPathComponent("__init__.py")
        return FileManager.default.fileExists(atPath: initFile.path)
    }

    /// Remove the plugin
    static func uninstall() {
        let pluginDir = FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent(".hermes/plugins/hermes_island")
        try? FileManager.default.removeItem(at: pluginDir)
    }
}
