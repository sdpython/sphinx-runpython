import glob
import io
import os
from typing import List, Optional, Sequence, Union


def images2pdf(
    images: Union[str, Sequence[str]],
    output: Optional[str],
    zoom: float = 1,
    rotate: float = 0,
    verbose: int = 0,
) -> List[str]:
    """
    Merges multiples images into one single pdf.
    Relies on :epkg:`img2pdf`. If an image name contains
    ``'*'``, the function assumes it is a pattern and
    uses :mod:`glob`.

    :param images: images to merge, it can be a comma separated values or a folder
    :param zoom: reduce or make the image bigger
    :param rotate: rotate the image
    :param output: output filename or stream
    :param verbose: verbosity

    Note:

    Using img2pdf directly is probably better.

    ::

        python -m img2pdf --output doc.pdf img/* -S A4 --auto-orient
    """
    from img2pdf import convert, Rotation

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

    all_images.sort()
    if zoom != 1 or rotate != 0:
        # See https://github.com/myollie/img2pdf/blob/master/src/img2pdf.py
        from PIL import Image
        from img2pdf import get_layout_fun, FitMode

        layout_fun = get_layout_fun(
            pagesize=(595.2755905511812, 841.8897637795276),
            imgsize=None,
            border=None,
            fit=FitMode.into,
            auto_orient=True,
        )

        data = []
        for img in all_images:
            im = Image.open(img)
            ext = os.path.splitext(img)[-1].lower()
            fmt = Image.EXTENSION[ext]
            if zoom != 1:
                size0 = im.size
                size = tuple(int(s * zoom) for s in size0)
                if verbose:
                    print(f"resizes from {size0} to {size} (formt={fmt!r}) for {img!r}")
                im = im.resize(size)
            if rotate != 0:
                if verbose:
                    print(f"rotates {rotate} (formt={fmt!r}) for {img!r}")
                im = im.rotate(rotate)
            buffer = io.BytesIO()
            im.save(buffer, format=fmt)
            data.append(buffer.getvalue())
        all_images = data

    for img in all_images:
        assert not isinstance(img, str) or os.path.exists(
            img
        ), f"Unable to find image {img!r}."

    try:
        convert(
            all_images,
            outputstream=st,
            rotation=Rotation.auto,
            layout_fun=layout_fun,
        )
    except TypeError as e:
        raise TypeError(
            f"Unable to process container type {type(all_images)} "
            f"and type {type(all_images[0])}."
        ) from e

    if close:
        st.close()

    return all_images
