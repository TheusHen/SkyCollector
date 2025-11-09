using JSON
using Images
using BlobTracking

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

    # Mock moon phase for now, as it's a more complex analysis
    moon_phase = "Waning Gibbous (mocked)"

    analysis_data = Dict(
        "stars" => stars,
        "moon_phase" => moon_phase
    )

    return JSON.json(analysis_data)
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
