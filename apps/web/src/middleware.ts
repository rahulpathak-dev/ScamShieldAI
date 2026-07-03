import { NextRequest, NextResponse } from "next/server";

const protectedPrefixes = ["/dashboard", "/analyzer", "/history", "/profile", "/admin", "/analyst"];
const authCookieName = "scamshield_access_token";

export function middleware(request: NextRequest) {
  const isProtectedPath = protectedPrefixes.some((prefix) => request.nextUrl.pathname.startsWith(prefix));
  if (!isProtectedPath) {
    return NextResponse.next();
  }

  const hasAuthCookie = Boolean(request.cookies.get(authCookieName)?.value);
  if (hasAuthCookie) {
    return NextResponse.next();
  }

  const loginUrl = new URL("/login", request.url);
  loginUrl.searchParams.set("next", request.nextUrl.pathname);
  return NextResponse.redirect(loginUrl);
}

export const config = {
  matcher: ["/dashboard/:path*", "/analyzer/:path*", "/history/:path*", "/profile/:path*", "/admin/:path*", "/analyst/:path*"]
};