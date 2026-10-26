using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using SharpDul.Pocket;
using SharpDul.Pocket.Localization;
using SharpDul.Pocket.Services;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

builder.Services.AddScoped(sp => new HttpClient { BaseAddress = new Uri(builder.HostEnvironment.BaseAddress) });
builder.Services.AddScoped<ContentLibrary>();
builder.Services.AddScoped<ProgressStore>();
builder.Services.AddScoped<Localizer>();

await builder.Build().RunAsync();
