# Client Library for encoding Videos with HeyWatch #

HeyWatch is a Video Encoding Web Service.

For a CLI, look at the ruby version: http://github.com/particles/heywatch-ruby

For more information:

* HeyWatch: http://heywatch.com 
* API Documentation: http://dev.heywatch.com
* Contact: [heywatch at particle-s.com](mailto:heywatch at particle-s.com)
* Twitter: [@particles](http://twitter.com/particles) / [@sadikzzz](http://twitter.com/sadikzzz)

## Install ##

	sudo easy_install heywatch

## Usage ##

	import heywatch
	
	# login with your HeyWatch username and password
	hw = heywatch.API(username, passwd)
	
	# get all your videos
	hw.all('video')
	
	➔ [
			{
	    	"created_at": "2011-06-15T12:05:25+02:00",
		    "title": "d41d8cd98f00b204e9800998ecf8427e",
		    "specs": {
		      "audio": {
		        "sample_rate": 24000,
		        "synched": true,
		        "stream": 0.1,
		        "codec": "aac",
		        "bitrate": 0,
		        "channels": 2
		      },
		      "size": 318,
		      "thumb": "http://raw-2.heywatch.com/5978aa591569a2e5e47805c8c008b1a2/CGI.29806.0.jpg",
		      "mime_type": "video/mp4",
		      "video": {
		        "stream": 0.0,
		        "codec": "mpeg4",
		        "container": "mov",
		        "aspect": 1.33,
		        "bitrate": 501,
		        "height": 240,
		        "length": 5,
		        "fps": 0.0,
		        "width": 320
		      }
		    },
		    "updated_at": "2011-06-15T12:05:25+02:00",
		    "id": 9662090
	  }
	]
	
	# get information about a specific video
	hw.info('video', 9662090)

### Create a download ###

	hw.create('download', url='http://site.com/yourvideo.mp4', title='yourtitle')

	➔ {
	  "created_at": "2011-06-15T19:00:11+02:00",
	  "error_msg": null,
	  "title": "yourtitle",
	  "video_id": 0,
	  "updated_at": "2011-06-15T19:00:11+02:00",
	  "url": "http://site.com/yourvideo.mp4",
	  "progress": {
	    "current_length": 0,
	    "speed": 0,
	    "percent": 0,
	    "time_left": "??"
	  },
	  "id": 4950011,
	  "error_code": null,
	  "length": 0,
	  "status": "pending"
	}

### Create a job ###
	
	hw.create('job', video_id=9662090, format_id=31, keep_video_size=True, ping_url_after_encode='http://yoursite.com/ping/heywatch?postid=123434', s3_directive='s3://accesskey:secretkey@myvideobucket/flv/123434.flv')
	
	➔ {
	  "ping_url_after_encode": "http://yoursite.com/ping/heywatch?postid=123434",
	  "cf_directive": null,
	  "error_msg": null,
	  "created_at": "2011-06-15T12:13:13+02:00",
	  "video_id": 9662090,
	  "updated_at": "2011-06-15T12:13:13+02:00",
	  "progress": 0,
	  "ping_url_if_error": null,
	  "s3_directive": "s3://accesskey:secretkey@myvideobucket/flv/123434.flv",
	  "format_id": 31,
	  "id": 4944088,
	  "error_code": null,
	  "ftp_directive": null,
	  "encoded_video_id": 0,
	  "encoding_options": {
	    "keep_video_size": true
	  },
	  "status": "pending",
	  "http_upload_directive": null
	}
	
### Delete a video ###

	hw.delete('video', 9662090)
	
	➔ True
	
### Generating thumbnails ###

	# Will return the binary data directly
	hw.jpg(9662142)
	hw.jpg(9662142, start=4)
	
	# Async method, you'll receive the thumbnails to 
	# your s3 account and get pinged when it's done
	hw.jpg(9662142, async=true, number=6, s3_directive='s3://accesskey:secretkey@mybucket/thumbnails/', ping_url='http://site.com/ping/heywatch/thumbs')
	
	➔ True

### Errors ###

	hw.create('download', url='not_a_valid_url')
	
	➔ heywatch.api.BadRequest: '400 {"message":"Url is invalid"}'

Released under the [MIT license](http://www.opensource.org/licenses/mit-license.php).