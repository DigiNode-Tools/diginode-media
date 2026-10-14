import CoreImage
import AppKit
let f = CIFilter(name: "CIQRCodeGenerator")!
f.setValue(CommandLine.arguments[1].data(using: .ascii), forKey: "inputMessage")
f.setValue("H", forKey: "inputCorrectionLevel")
let img = f.outputImage!
let cg = CIContext().createCGImage(img, from: img.extent)!
let rep = NSBitmapImageRep(cgImage: cg)
for y in 0..<rep.pixelsHigh { var s = ""; for x in 0..<rep.pixelsWide { s += (rep.colorAt(x: x, y: y)!.brightnessComponent < 0.5) ? "1" : "0" }; print(s) }
