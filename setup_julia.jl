#!/usr/bin/env julia

# Julia package installation and precompilation script
# This ensures all required packages are installed and precompiled before running the analysis

println("Installing and precompiling Julia packages...")

using Pkg

# Add required packages
packages = ["JSON", "Images", "BlobTracking", "AstroLib"]

println("Checking and installing packages...")
for pkg in packages
    try
        println("  - Checking $pkg...")
        Pkg.add(pkg)
    catch e
        println("  ! Error installing $pkg: ", e)
        exit(1)
    end
end

println("\nPrecompiling all packages...")
try
    Pkg.precompile()
    println("✓ All packages precompiled successfully!")
catch e
    println("! Error during precompilation: ", e)
    exit(1)
end

println("\nTesting package imports...")
try
    using JSON
    using Images
    using BlobTracking
    using AstroLib
    println("✓ All packages imported successfully!")
catch e
    println("! Error importing packages: ", e)
    exit(1)
end

println("\n✓ Setup complete! Julia environment is ready.")
