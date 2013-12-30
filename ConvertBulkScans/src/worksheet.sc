import javax.swing._;
import javax.imageio.ImageIO;
import java.io.File;
import java.awt.image.BufferedImage;
import java.awt.Image;
import scala.sys.process._;
import scala.util._;
import scala.math._;

object test {
	val filenames = convertScans.getImageFilenamesInDirectory("/home/chad/work/apma507_scans").take(3)
                                                  //> filenames  : Array[String] = Array(/home/chad/work/apma507_scans/out1-16.jpg
                                                  //| , /home/chad/work/apma507_scans/out44-43.jpg, /home/chad/work/apma507_scans/
                                                  //| out1-28.jpg)
	val stdevs = convertScans.getImageStandardDeviations(filenames.toList)
                                                  //> stdevs  : List[Double] = List(13771.8, 3145.92, 12858.6)
	val objs = filenames.zip(stdevs).map({case (x, y) => new imageData(x, y)})
                                                  //> objs  : Array[imageData] = Array([/home/chad/work/apma507_scans/out1-16.jpg 
                                                  //| 13771.8 None None], [/home/chad/work/apma507_scans/out44-43.jpg 3145.92 None
                                                  //|  None], [/home/chad/work/apma507_scans/out1-28.jpg 12858.6 None None])
  val objs_shuffle = Random.shuffle(objs.toList).take(min(10, objs.length))
                                                  //> objs_shuffle  : List[imageData] = List([/home/chad/work/apma507_scans/out1-1
                                                  //| 6.jpg 13771.8 None None], [/home/chad/work/apma507_scans/out1-28.jpg 12858.6
                                                  //|  None None], [/home/chad/work/apma507_scans/out44-43.jpg 3145.92 None None])
                                                  //| 
	val explicit_blank = objs_shuffle.map(x => convertScans.isImageBlankExplicit(x.filename))
                                                  //> explicit_blank  : List[Boolean] = List(false, false, true)|
}

object convertScans {
	def isImageBlankExplicit(filename : String) : Boolean  = {
		val img = ImageIO.read(new File(filename));
	  val scaled_img = img.getScaledInstance(img.getWidth() / 4, img.getHeight() / 4, Image.SCALE_SMOOTH);
	  val icon = new ImageIcon(scaled_img)
		val opts : Array[Object] = Array("Yes", "No")
		val n = JOptionPane.showOptionDialog(null, "Is blank?", "Is blank?",
			 JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE, icon, opts, opts(0));
		return n == 0
	}
	
	def getImageStandardDeviations(filenames : List[String]) : List[Double] = {
		val identify_cmd = "identify -format %[standard-deviation]\\n " + filenames.reduceLeft((x, y) => x + " " + y)
	  return identify_cmd.!!.split("\n").toList.map(x => x.toDouble)
	}
	
	def getImageFilenamesInDirectory(dir : String) : Array[String] =
		return new File(dir).listFiles.map(x => x.getPath).filter(x => x.endsWith(".jpg"))
}

class imageData(val filename: String,
	val stdDev: Double,
	val isBlankExplicit : Option[Boolean] = None,
	val probBlank : Option[Double]= None) {
	override def toString(): String =
		return "[" + filename + " " + stdDev.toString + " " + isBlankExplicit.toString + " " + probBlank.toString + "]"
}