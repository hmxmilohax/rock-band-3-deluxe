use clap::Parser;
use std::error::Error;
use std::path::Path;

#[derive(clap::Parser)]
struct Args {
    input_file: Box<Path>,
    output_file: Box<Path>,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = Args::parse();

    let mut buf = std::fs::read(args.input_file)?;

    for i in (32..buf.len()).step_by(2) {
        let byte1 = buf[i];
        let byte2 = buf[i + 1];

        buf[i] = byte2;
        buf[i + 1] = byte1;
    }

    std::fs::write(args.output_file, buf)?;

    Ok(())
}