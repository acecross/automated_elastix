from image_operations import ImageStuff
from facade import TransformElastix

EXPECTED_EXPASION = 3
path1 =
path2 = 


if __name__ == '__main__':
    image_op = ImageStuff()
    transform = TransformElastix()
    transform.fixed_image = path1
    resized = image_op.resize_image(path2, EXPECTED_EXPASION)
    transform.moving_image = resized
    #run similarity transform
    transform.similarity_transform()
    similarity_image = transform.result_image
    TP = transform.STP
    image_op.show_overlay(transform.fixed_image, similarity_image, scale=EXPECTED_EXPASION, TP=TP)
    #run spline transform
    transform.moving_image = similarity_image
    transform.b_spline_tranform()
    b_spline_image = transform.result_image
    image_op.show_overlay(transform.fixed_image, b_spline_image, scale=EXPECTED_EXPASION, TP=TP)


    image_op.show_overlay(transform.fixed_image, similarity_image,
                          scale=EXPECTED_EXPASION, vec_map=transform.get_distortion_map(), TP=TP)

