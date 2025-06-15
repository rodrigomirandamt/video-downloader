"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import {
  Download,
  Youtube,
  Twitter,
  AlertCircle,
  CheckCircle2,
  Loader2,
  Sword,
  Shield,
  Zap,
  Crown,
  Gem,
} from "lucide-react"
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
      return "Invalid URL detected! Please enter a valid YouTube or X (Twitter) URL to continue your quest."
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
      await new Promise((resolve) => setTimeout(resolve, 3000))
      setProgress(100)
      setSuccess("Quest completed! Media successfully captured and added to your inventory!")
    } catch (err) {
      setError("Quest failed! The download spell was interrupted. Try casting again.")
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
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        {/* Main Title */}
        <div className="text-center mb-12">
          <div className="flex justify-center items-center gap-4 mb-6">
            <div className="p-4 bg-gradient-to-r from-red-600 to-red-700 rounded-xl shadow-lg border border-red-500/30">
              <Sword className="h-10 w-10 text-white" />
            </div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-red-400 via-red-300 to-orange-400 bg-clip-text text-transparent">
              MediaSlayer
            </h1>
            <div className="p-4 bg-gradient-to-r from-blue-600 to-blue-700 rounded-xl shadow-lg border border-blue-500/30">
              <Shield className="h-10 w-10 text-white" />
            </div>
          </div>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto leading-relaxed">
            Embark on your digital quest to capture and download legendary media from the realms of YouTube and X.{" "}
            <span className="text-red-400 font-semibold">Forge your collection!</span>
          </p>
        </div>

        {/* Main Quest Card */}
        <Card className="shadow-2xl border border-slate-700/50 bg-gradient-to-br from-slate-800/90 to-slate-900/90 backdrop-blur-sm">
          <CardHeader className="text-center pb-6 border-b border-slate-700/50">
            <div className="flex justify-center mb-4">
              <div className="p-3 bg-gradient-to-r from-red-600 to-red-700 rounded-full">
                <Download className="h-6 w-6 text-white" />
              </div>
            </div>
            <CardTitle className="text-2xl font-bold text-white">Begin Your Quest</CardTitle>
            <CardDescription className="text-gray-400">
              Enter the URL of your target media and select your preferred enchantment
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-6 p-6">
            {/* URL Input */}
            <div className="space-y-3">
              <label className="text-sm font-medium text-gray-300 flex items-center gap-2">
                <Zap className="h-4 w-4 text-yellow-400" />
                Target URL
              </label>
              <div className="relative">
                <Input
                  type="url"
                  placeholder="https://youtube.com/watch?v=... or https://x.com/..."
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="pl-12 h-12 text-lg bg-slate-700/50 border-slate-600 text-white placeholder:text-gray-400 focus:border-red-500 focus:ring-red-500/20 transition-all"
                />
                <div className="absolute left-3 top-1/2 transform -translate-y-1/2">
                  {platform === "youtube" && <Youtube className="h-6 w-6 text-red-500" />}
                  {platform === "twitter" && <Twitter className="h-6 w-6 text-blue-400" />}
                  {!platform && <Download className="h-6 w-6 text-gray-500" />}
                </div>
              </div>

              {platform && (
                <div className="flex justify-center">
                  <Badge className="bg-gradient-to-r from-red-600 to-red-700 text-white border-red-500/30">
                    <Sword className="h-3 w-3 mr-1" />
                    {platform === "youtube" ? "YouTube" : "X (Twitter)"} realm detected
                  </Badge>
                </div>
              )}
            </div>

            {/* Enchantment Selection */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300 flex items-center gap-2">
                  <Gem className="h-4 w-4 text-purple-400" />
                  Format Enchantment
                </label>
                <Select value={format} onValueChange={setFormat}>
                  <SelectTrigger className="h-11 bg-slate-700/50 border-slate-600 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-800 border-slate-700">
                    <SelectItem value="mp4" className="text-white hover:bg-slate-700">
                      ⚔️ MP4 (Video Scroll)
                    </SelectItem>
                    <SelectItem value="mp3" className="text-white hover:bg-slate-700">
                      🎵 MP3 (Audio Rune)
                    </SelectItem>
                    <SelectItem value="webm" className="text-white hover:bg-slate-700">
                      🛡️ WebM (Web Armor)
                    </SelectItem>
                    <SelectItem value="wav" className="text-white hover:bg-slate-700">
                      🔮 WAV (Crystal Audio)
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300 flex items-center gap-2">
                  <Crown className="h-4 w-4 text-yellow-400" />
                  Quality Level
                </label>
                <Select value={quality} onValueChange={setQuality}>
                  <SelectTrigger className="h-11 bg-slate-700/50 border-slate-600 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-800 border-slate-700">
                    <SelectItem value="1080p" className="text-white hover:bg-slate-700">
                      👑 1080p (Legendary)
                    </SelectItem>
                    <SelectItem value="720p" className="text-white hover:bg-slate-700">
                      ⭐ 720p (Epic)
                    </SelectItem>
                    <SelectItem value="480p" className="text-white hover:bg-slate-700">
                      🔸 480p (Rare)
                    </SelectItem>
                    <SelectItem value="360p" className="text-white hover:bg-slate-700">
                      ⚪ 360p (Common)
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Progress Bar */}
            {isLoading && (
              <div className="space-y-3">
                <div className="flex justify-between text-sm text-gray-300">
                  <span className="flex items-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin text-red-400" />
                    Casting download spell...
                  </span>
                  <span className="text-red-400 font-bold">{Math.round(progress)}%</span>
                </div>
                <Progress value={progress} className="h-3 bg-slate-700" />
              </div>
            )}

            {/* Error Alert */}
            {error && (
              <Alert className="border-red-500/50 bg-red-900/20 text-red-300">
                <AlertCircle className="h-4 w-4 text-red-400" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {/* Success Alert */}
            {success && (
              <Alert className="border-green-500/50 bg-green-900/20 text-green-300">
                <CheckCircle2 className="h-4 w-4 text-green-400" />
                <AlertDescription>{success}</AlertDescription>
              </Alert>
            )}

            {/* Download Button */}
            <Button
              onClick={handleDownload}
              disabled={!url || isLoading}
              className="w-full h-14 text-lg font-bold bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white border border-red-500/30 shadow-lg transition-all duration-200 transform hover:scale-[1.02] hover:shadow-red-500/25"
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Casting Spell...
                </>
              ) : (
                <>
                  <Sword className="mr-2 h-5 w-5" />
                  Execute Download Quest
                </>
              )}
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
