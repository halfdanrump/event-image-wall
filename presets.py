import image_pipelines as ip

ip.use_brewer_background(image, ip.sketch, gain = 1, mode_size = 30).show()
ip.use_brewer_background(image, ip.sketch, gain = 5, mode_size = 30).show()
ip.use_brewer_background(image, ip.sketch, gain = 2, mode_size = 11).show()

ip.color_filter(image, '3c5c47', 'b0e4e0').show()
ip.use_brewer_background(image, ip.sketch).show()
ip.use_brewer_background(image, ip.monochrome).show()
