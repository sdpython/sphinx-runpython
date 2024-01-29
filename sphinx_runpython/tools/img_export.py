import glob
import os
from typing import List, Optional, Sequence, Union


def images2pdf(
    images: Union[str, Sequence[str]], output: Optional[str], verbose: int = 0
) -> List[str]:
    """
    Merges multiples images into one single pdf.
    Relies on :epkg:`img2pdf`. If an image name contains
    ``'*'``, the function assumes it is a pattern and
    uses :mod:`glob`.

    :param images: images to merge, it can be a comma separated values or a folder
    :param output: output filename or stream
    :param verbose: verbosity
    """
    from img2pdf import convert

    if isinstance(images, str):
        if "," in images:
            images = images.split(",")
        elif "*" in images:
            images = [images]
        elif os.path.exists(images):
            images = [images]
        else:
            raise RuntimeError(f"Unable to deal with images={images!r}")
    elif not isinstance(images, (list, tuple)):
        raise TypeError("Images must be a list.")  # pragma: no cover

    all_images = []
    for img in images:
        if "*" in img:
            if verbose:
                print(f"[images2pdf] look into {img!r}")
            names = glob.glob(img)
            if verbose:
                print(f"[images2pdf] add {len(names)} images")
            all_images.extend(names)
        else:
            if verbose:
                print(f"[images2pdf] add {img!r}")
            all_images.append(img)

    if verbose > 1:
        for i, img in enumerate(all_images):
            print(f"[images2pdf] {i + 1}/{len(all_images)} {img!r}")

    st, close = (
        (open(output, "wb"), True) if isinstance(output, str) else (output, False)
    )

    for img in all_images:
        assert not isinstance(img, str) or os.path.exists(
            img
        ), f"Unable to find image {img!r}."

    try:
        convert(all_images, outputstream=st, with_pdfrw=False)
    except TypeError as e:
        raise TypeError(
            f"Unable to process container type {type(all_images)} and type {type(all_images[0])}."
        )

    if close:
        st.close()

    return all_images
