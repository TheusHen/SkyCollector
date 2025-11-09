using JSON
using Images
using BlobTracking
using AstroLib
using Dates

function analyze_image(image_path)
    println(stderr, "[Julia] Loading image from: ", image_path)
    
    # Load the image
    img = load(image_path)
    println(stderr, "[Julia] Image loaded successfully, size: ", size(img))

    # Convert to grayscale
    img_gray = Gray.(img)
    println(stderr, "[Julia] Converted to grayscale")

    # Detect blobs (stars)
    # blob_LoG requires σscales as second parameter (scale range for detection)
    # Using a range of scales from 1 to 10 pixels for star detection
    println(stderr, "[Julia] Starting blob detection...")
    σscales = 1:10
    blobs = blob_LoG(img_gray, σscales, rthresh=0.1)
    println(stderr, "[Julia] Detected ", length(blobs), " blobs (stars)")

    # Format the star data
    stars = []
    for (i, blob) in enumerate(blobs)
        push!(stars, Dict(
            "id" => i,
            "x" => blob.location[2],
            "y" => blob.location[1],
            "brightness" => blob.amplitude
        ))
    end

    # Calculate moon phase
    println(stderr, "[Julia] Calculating moon phase...")
    jd = jdcnv(now())
    moon_phase_val = mphase(jd)
    moon_phase_str = moon_phase_string(moon_phase_val)
    println(stderr, "[Julia] Moon phase: ", moon_phase_str, " (", round(moon_phase_val, digits=4), ")")

    analysis_data = Dict(
        "stars" => stars,
        "moon_phase" => moon_phase_str
    )

    println(stderr, "[Julia] Analysis complete")
    return JSON.json(analysis_data)
end

function moon_phase_string(phase_val)
    if phase_val < 0.0625 || phase_val >= 0.9375
        return "New Moon"
    elseif phase_val < 0.1875
        return "Waxing Crescent"
    elseif phase_val < 0.3125
        return "First Quarter"
    elseif phase_val < 0.4375
        return "Waxing Gibbous"
    elseif phase_val < 0.5625
        return "Full Moon"
    elseif phase_val < 0.6875
        return "Waning Gibbous"
    elseif phase_val < 0.8125
        return "Last Quarter"
    else
        return "Waning Crescent"
    end
end

function main()
    if length(ARGS) != 1
        println(stderr, "Usage: julia analyze.jl <image_path>")
        exit(1)
    end

    image_path = ARGS[1]

    if !isfile(image_path)
        println(stderr, "Error: File not found at ", image_path)
        exit(1)
    end

    json_output = analyze_image(image_path)
    println(json_output)
end

main()
