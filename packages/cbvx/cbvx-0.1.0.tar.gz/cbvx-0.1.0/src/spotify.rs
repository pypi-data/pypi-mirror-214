use color_thief::{get_palette, ColorFormat};
use image::{io::Reader, DynamicImage, GenericImage, GenericImageView};
use pyo3::{prelude::*, types::PyBytes};
use std::io::Cursor;

#[pyclass]
#[derive(Debug)]
pub struct Color {
    #[pyo3(get)]
    pub r: u8,
    #[pyo3(get)]
    pub g: u8,
    #[pyo3(get)]
    pub b: u8,
}

impl Color {
    fn new(r: u8, g: u8, b: u8) -> Self {
        Self { r, g, b }
    }
}

#[pyclass]
pub struct Spotify {
    image: DynamicImage,
    shift: u8,
    constrast: f32,
    rate: f32,
}

#[pymethods]
impl Spotify {
    #[new]
    fn new(img: &[u8]) -> Self {
        let cursor = Cursor::new(img);
        // Convert the buffer to a DynamicImage (spotify image is resized to 300x300)
        let mut img = Reader::new(cursor);
        img.set_format(image::ImageFormat::Png);
        let img = img
            .decode()
            .expect("could not decode buffer to dynamic image")
            .thumbnail(300, 300);
        Self {
            image: img,
            shift: 0,
            constrast: 20.0,
            rate: 0.5,
        }
    }

    fn shift(&mut self, shift: u8) {
        assert!(shift <= 5);
        self.shift = shift;
    }

    fn contrast(&mut self, contrast: f32) {
        assert!(contrast <= 50.0);
        self.constrast = contrast;
    }

    fn rate(&mut self, rate: f32) {
        assert!(rate >= 0.0 && rate <= 10.0);
        self.rate = rate;
    }

    fn growth_rate(&self, linear: f32) -> f32 {
        linear.powf(self.rate)
    }

    fn pallet(&self) -> PyResult<(Color, Color)> {
        let pallet = get_palette(self.image.as_bytes(), ColorFormat::Rgb, 1, self.shift + 2)
            .expect("Could not generate pallet from image");
        let (c1, c2) = (
            pallet[0 + self.shift as usize],
            pallet[1 + self.shift as usize],
        );

        Ok((Color::new(c1.r, c1.g, c1.b), Color::new(c2.r, c2.g, c2.b)))
    }

    fn get_base(&self) -> PyResult<Py<PyBytes>> {
        // Create a 600x300 blank image
        let mut blank = image::DynamicImage::new_rgb8(600, 300);

        // Get the background color
        let (bg, _) = self.pallet()?;

        // Fill blank image with solid bg color
        for x in 0..blank.width() {
            for y in 0..blank.height() {
                blank.put_pixel(x, y, image::Rgba::from([bg.r, bg.g, bg.b, 255]));
            }
        }

        // Increase contrast
        blank = blank.adjust_contrast(self.constrast);

        // Get new contrasted color from 0, 0 pixel
        let tpx = blank.get_pixel(0, 0);
        let bg = Color::new(tpx[0], tpx[1], tpx[2]);

        // Do the interpolation
        for x in 0..blank.width() {
            // Linear from 1 to 0
            let mut dec_per = (600.0 - x as f32).abs() / 300.0;
            // Logarithmic from 1 to 0
            dec_per = self.growth_rate(dec_per);
            // Interpolate
            for y in 0..blank.height() {
                if x > 299 {
                    let opx = self.image.get_pixel(x - 300, y);
                    let opx = (opx.0[0], opx.0[1], opx.0[2]);
                    let clr = [
                        (opx.0 as f32 + (bg.r as i32 - opx.0 as i32) as f32 * dec_per) as u8,
                        (opx.1 as f32 + (bg.g as i32 - opx.1 as i32) as f32 * dec_per) as u8,
                        (opx.2 as f32 + (bg.b as i32 - opx.2 as i32) as f32 * dec_per) as u8,
                        255,
                    ];
                    blank.put_pixel(x, y, image::Rgba::from(clr));
                }
            }
        }

        // Done
        Python::with_gil(|py| {
            let bytes = PyBytes::new(py, &*blank.into_bytes()).into();
            Ok(bytes)
        })
    }
}
