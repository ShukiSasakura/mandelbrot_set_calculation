use clap::Parser;
use num::Complex;
use std::thread;
use std::time::Instant;
use image::ColorType;
use image::png::PNGEncoder;
use std::fs::File;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    #[arg(short, long)]
    width: usize,
    #[arg(short, long)]
    height: usize,
    #[arg(short, long)]
    thread_num: usize,
}

fn main() {
    let args = Args::parse();

    let bounds = (args.width, args.height);
    let upper_left = Complex { re: -1.0, im: 1.0};
    let lower_right = Complex { re: 1.0, im: -1.0};

    let mut pixels = vec![0; bounds.0 * bounds.1];

    // 計算時間計測開始
    let start_time = Instant::now();

    // ピクセルをわけ，各スレッドで計算
    thread::scope(|s| {
        let threads = args.thread_num;
        let rows_per_band = bounds.1 / threads + 1;
        let bands: Vec<&mut [u8]> = pixels.chunks_mut(rows_per_band * bounds.0).collect();

        for (i, band) in bands.into_iter().enumerate() {
            //let mut band_cloned = band.to_vec();
            let top = rows_per_band * i;
            let height = band.len() / bounds.0;
            let band_bounds = (bounds.0, height);
            let band_upper_left = pixel_to_point(bounds, (0, top), upper_left, lower_right);
            let band_lower_right = pixel_to_point(bounds, (bounds.0, top + height), upper_left, lower_right);

            s.spawn(move || {
                render(band, band_bounds, band_upper_left, band_lower_right);
            });
        }
    });

    //println!("{:?}", pixels);

    // 計算時間を出力
    let elapsed = start_time.elapsed();
    let elapsed_time = elapsed.as_nanos() as f64;
    let elapsed_time = elapsed_time / 1000000000.0;

    println!("{:?}", elapsed_time);

    let _ = write_image("mandelbrot.png", &mut pixels, bounds);
}

fn escape_time(c: Complex<f64>, limit: u32) -> Option<u32> {
    let mut z = Complex {re: 0.0, im: 0.0};

    for i in 0..limit {
        z = z * z + c;
        if z.norm_sqr() > 4.0 {
            return Some(i);
        }
    }

    None
}

fn pixel_to_point(bounds: (usize, usize),
                  pixel: (usize, usize),
                  upper_left: Complex<f64>,
                  lower_right: Complex<f64>)
    -> Complex<f64>
{
    let (complex_plane_width, complex_plane_height) = (lower_right.re - upper_left.re,
                                                       upper_left.im - lower_right.im);
    Complex {
        re: upper_left.re + pixel.0 as f64 * complex_plane_width / bounds.0 as f64,
        im: upper_left.im - pixel.1 as f64 * complex_plane_height / bounds.1 as f64 }

}

fn render(pixels: &mut [u8],
          bounds: (usize, usize),
          upper_left: Complex<f64>,
          lower_right: Complex<f64>)
{
    assert!(pixels.len() == bounds.0 * bounds.1);

    for row in 0..bounds.1 {
        for column in 0..bounds.0 {
            let point = pixel_to_point(bounds, (column, row), upper_left, lower_right);
            pixels[row * bounds.0 + column] = match escape_time(point, 255) {
                None => 0,
                Some(count) => 255 - count as u8
            };
        }
    }
}

fn write_image(filename: &str, pixels: &mut Vec<u8>, bounds: (usize, usize)) -> Result<(), std::io::Error>
{
    let output = File::create(filename)?;

    let encoder = PNGEncoder::new(output);
    encoder.encode(&pixels, bounds.0 as u32, bounds.1 as u32, ColorType::Gray(8))?;
    Ok(())
}
