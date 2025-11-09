using JSON
using Images
using BlobTracking
using AstroLib
using Dates

function analyze_image(image_path)
    # Load the image
    img = load(image_path)

    # Convert to grayscale
    img_gray = Gray.(img)

    # Detect blobs (stars)
    blobs = blob_LoG(img_gray, 0.1, [10])

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
    jd = jdcnv(now())
    moon_phase_val = moonph(jd)
    moon_phase_str = moon_phase_string(moon_phase_val)

    analysis_data = Dict(
        "stars" => stars,
        "moon_phase" => moon_phase_str
    )

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
