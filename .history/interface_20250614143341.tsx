"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Download, Youtube, Twitter, AlertCircle, CheckCircle2, Loader2 } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"

export default function MediaDownloader() {
  const [url, setUrl] = useState("")
  const [format, setFormat] = useState("mp4")
  const [quality, setQuality] = useState("720p")
  const [isLoading, setIsLoading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")

  const detectPlatform = (url: string) => {
    if (url.includes("youtube.com") || url.includes("youtu.be")) {
      return "youtube"
    } else if (url.includes("twitter.com") || url.includes("x.com")) {
      return "twitter"
    }
    return null
  }

  const validateUrl = (url: string) => {
    const platform = detectPlatform(url)
    if (!platform) {
      return "Please enter a valid YouTube or X (Twitter) URL"
    }
    return null
  }

  const handleDownload = async () => {
    setError("")
    setSuccess("")

    const validationError = validateUrl(url)
    if (validationError) {
      setError(validationError)
      return
    }

    setIsLoading(true)
    setProgress(0)

    // Simulate download progress
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval)
          return 90
        }
        return prev + Math.random() * 15
      })
    }, 200)

    try {
      // Here you would implement the actual download logic
      // This is just a simulation
      await new Promise((resolve) => setTimeout(resolve, 3000))

      setProgress(100)
      setSuccess("Download completed successfully!")

      // In a real implementation, you would trigger the actual file download here
      // For example: window.open(downloadUrl, '_blank')
    } catch (err) {
      setError("Download failed. Please try again.")
    } finally {
      setIsLoading(false)
      clearInterval(progressInterval)
      setTimeout(() => {
        setProgress(0)
        setSuccess("")
      }, 3000)
    }
  }

  const platform = detectPlatform(url)

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center items-center gap-3 mb-4">
            <div className="p-3 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl">
              <Download className="h-8 w-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              MediaGrab
            </h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Download videos and media from YouTube and X (Twitter) with ease. Fast, simple, and completely free.
          </p>
        </div>

        {/* Main Card */}
        <Card className="max-w-2xl mx-auto shadow-xl border-0 bg-white/80 backdrop-blur-sm">
          <CardHeader className="text-center pb-6">
            <CardTitle className="text-2xl font-semibold text-gray-800">Download Your Media</CardTitle>
            <CardDescription className="text-gray-600">
              Paste your YouTube or X URL below and choose your preferred format
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-6">
            {/* URL Input */}
            <div className="space-y-2">
              <div className="relative">
                <Input
                  type="url"
                  placeholder="https://youtube.com/watch?v=... or https://x.com/..."
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="pl-12 h-12 text-lg border-2 focus:border-blue-500 transition-colors"
                />
                <div className="absolute left-3 top-1/2 transform -translate-y-1/2">
                  {platform === "youtube" && <Youtube className="h-6 w-6 text-red-500" />}
                  {platform === "twitter" && <Twitter className="h-6 w-6 text-blue-500" />}
                  {!platform && <Download className="h-6 w-6 text-gray-400" />}
                </div>
              </div>

              {platform && (
                <div className="flex justify-center">
                  <Badge variant="secondary" className="capitalize">
                    {platform === "youtube" ? "YouTube" : "X (Twitter)"} detected
                  </Badge>
                </div>
              )}
            </div>

            {/* Format Selection */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">Format</label>
                <Select value={format} onValueChange={setFormat}>
                  <SelectTrigger className="h-11">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="mp4">MP4 (Video)</SelectItem>
                    <SelectItem value="mp3">MP3 (Audio)</SelectItem>
                    <SelectItem value="webm">WebM (Video)</SelectItem>
                    <SelectItem value="wav">WAV (Audio)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">Quality</label>
                <Select value={quality} onValueChange={setQuality}>
                  <SelectTrigger className="h-11">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1080p">1080p (Full HD)</SelectItem>
                    <SelectItem value="720p">720p (HD)</SelectItem>
                    <SelectItem value="480p">480p (SD)</SelectItem>
                    <SelectItem value="360p">360p (Low)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Progress Bar */}
            {isLoading && (
              <div className="space-y-2">
                <div className="flex justify-between text-sm text-gray-600">
                  <span>Downloading...</span>
                  <span>{Math.round(progress)}%</span>
                </div>
                <Progress value={progress} className="h-2" />
              </div>
            )}

            {/* Error Alert */}
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {/* Success Alert */}
            {success && (
              <Alert className="border-green-200 bg-green-50">
                <CheckCircle2 className="h-4 w-4 text-green-600" />
                <AlertDescription className="text-green-800">{success}</AlertDescription>
              </Alert>
            )}

            {/* Download Button */}
            <Button
              onClick={handleDownload}
              disabled={!url || isLoading}
              className="w-full h-12 text-lg font-semibold bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transition-all duration-200 transform hover:scale-[1.02]"
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Downloading...
                </>
              ) : (
                <>
                  <Download className="mr-2 h-5 w-5" />
                  Download Media
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        {/* Features */}
        <div className="max-w-4xl mx-auto mt-16">
          <h2 className="text-2xl font-bold text-center mb-8 text-gray-800">Why Choose MediaGrab?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="text-center p-6 border-0 bg-white/60 backdrop-blur-sm">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Download className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="font-semibold mb-2">Fast Downloads</h3>
              <p className="text-gray-600 text-sm">Lightning-fast downloads with optimized servers</p>
            </Card>

            <Card className="text-center p-6 border-0 bg-white/60 backdrop-blur-sm">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <CheckCircle2 className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="font-semibold mb-2">High Quality</h3>
              <p className="text-gray-600 text-sm">Download in multiple formats and resolutions</p>
            </Card>

            <Card className="text-center p-6 border-0 bg-white/60 backdrop-blur-sm">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Youtube className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="font-semibold mb-2">Multi-Platform</h3>
              <p className="text-gray-600 text-sm">Supports YouTube, X (Twitter), and more platforms</p>
            </Card>
          </div>
        </div>

        {/* Footer */}
        <footer className="text-center mt-16 text-gray-500 text-sm">
          <p>© 2024 MediaGrab. Built for personal use. Please respect content creators' rights.</p>
        </footer>
      </div>
    </div>
  )
}
